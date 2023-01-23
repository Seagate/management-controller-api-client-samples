#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing, please email
# opensource@seagate.com

from lxml import etree
from error import MCConnectionError, MCAuthenticationError
import requests
import six
import hashlib
import logging as LOG


class MCClient(object):
    def __init__(self, host, username, password, protocol, port, ssl_verify):
        self._mgmt_ip_addrs = host
        self._port = port
        self._username = username
        self._password = password
        self._protocol = protocol
        self._session_key = None
        self.ssl_verify = ssl_verify
        self._set_host(self._mgmt_ip_addrs)
        if not ssl_verify:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _set_host(self, ip_addr):
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
            not_responding = self._mgmt_ip_addrs
            LOG.exception('session_login failed to connect to %s',
                          self._mgmt_ip_addrs)
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
                              self._mgmt_ip_addrs)
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