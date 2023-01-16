import hashlib
import math
import time

from lxml import etree
import requests
import six

import logging as LOG


class MCException(Exception):
    message = 'An unknown exception occurred.'
    code = 0

    def __init__(self, message=None, code=0, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message
        self.code = int(code)

        for k, v in self.kwargs.items():
            if isinstance(v, Exception):
                self.kwargs[k] = six.text_type(v)

        if self._should_format():
            try:
                message = self.message % kwargs

            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception('Exception in string format operation')
                for name, value in kwargs.items():
                    LOG.error("%(name)s: %(value)s",
                              {'name': name, 'value': value})
                if CONF.fatal_exception_format_errors:
                    six.reraise(*exc_info)
                # at least get the core message out if something happened
                message = self.message
        elif isinstance(message, Exception):
            message = six.text_type(message)

        self.msg = message
        super(MCException, self).__init__(message)

    def _should_format(self):
        return self.kwargs['message'] is None or '%(message)' in self.message

    def __unicode__(self):
        return msg

# ConnectionErrors result from inability to communicate with array


class MCConnectionError(MCException):
    message = "%(message)s"

# AuthenticationErrors result from inability to communicate with array


class MCAuthenticationError(MCException):
    message = "%(message)s"

# RequestErorrs are raised when an operation fails on the array


class MCRequestError(MCException):
    message = "%(message)s"


class MCClient(object):
    def __init__(self, host, username, password, protocol='https', port=443, ssl_verify=False):
        self._mgmt_ip_addrs = list(map(str.strip, host.split(',')))
        self._port = port
        self._username = username
        self._password = password
        self._protocol = protocol
        self._session_key = None
        self.ssl_verify = ssl_verify
        self._set_host(self._mgmt_ip_addrs[0])
        self._luns_in_use_by_host = {}
        if not ssl_verify:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _set_host(self, ip_addr):
        self._curr_ip_addr = ip_addr
        self._base_url = "%s://%s:%d/api" % (self._protocol,
                                             ip_addr, self._port)

    def _get_auth_token(self, xml):
        """Parse an XML authentication reply to extract the session key."""
        self._session_key = None
        try:
            tree = etree.XML(xml)
            # The 'return-code' property is not valid in this context, so we
            # we check value of 'response-type-numeric' (0 => Success)
            rtn = tree.findtext(".//PROPERTY[@name='response-type-numeric']")
            session_key = tree.findtext(".//PROPERTY[@name='response']")
            if rtn == '0':
                self._session_key = session_key
        except Exception as e:
            msg = "Cannot parse session key: %s" % e.msg
            raise MCConnectionError(message=msg)

    def login(self):
        if self._session_key is None:
            return self.session_login()

    def session_login(self):
        """Authenticates the service on the device.

        Tries all the IP addrs listed in the san_ip parameter
        until a working one is found or the list is exhausted.
        """

        try:
            self._get_session_key()
            LOG.debug("Logged in to array at %s (session %s)",
                      self._base_url, self._session_key)
            return
        except MCConnectionError:
            not_responding = self._curr_ip_addr
            LOG.exception('session_login failed to connect to %s',
                          self._curr_ip_addr)
            # Loop through the remaining management addresses
            # to find one that's up.
            for host in self._mgmt_ip_addrs:
                if host is not_responding:
                    continue
                self._set_host(host)
                try:
                    self._get_session_key()
                    return
                except MCConnectionError:
                    LOG.error('Failed to connect to %s',
                              self._curr_ip_addr)
                    continue
        raise MCConnectionError(
            message="Failed to log in to management controller")

    def _get_session_key(self):
        """Retrieve a session key from the array."""

        self._session_key = None
        hash_ = "%s_%s" % (self._username, self._password)
        if six.PY3:
            hash_ = hash_.encode('utf-8')
        hash_ = hashlib.md5(hash_)
        digest = hash_.hexdigest()
        basic_auth = requests.auth.HTTPBasicAuth(
            self._username, self._password)
        url = self._base_url + "/login/" + digest
        # XXX url = self._base_url + '/login/ff719743d4f5b91a936e9c540c919e0632dbf884114dc0040a5e1f291edf15e3' # XXX
        try:
            LOG.debug("Attempting to log in to %s", url)
            if self._protocol == 'https':
                xml = requests.get(url, verify=self.ssl_verify, timeout=30,
                                   auth=(self._username, self._password))
            else:
                xml = requests.get(url, verify=self.ssl_verify, timeout=30)

        except requests.exceptions.RequestException:
            msg = "Failed to obtain MC session key"
            LOG.exception(msg)
            raise MCConnectionError(message=msg)

        LOG.debug("xml response to login request: \n%s",
                  xml.text.encode('UTF-8'))

        self._get_auth_token(xml.text.encode('utf8'))
        LOG.debug("session key = %s", self._session_key)
        print("Session Key = " + self._session_key + "\n")
        if self._session_key is None:
            raise MCAuthenticationError(
                message="Failed to get session key")
