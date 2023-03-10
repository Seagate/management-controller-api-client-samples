#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the Apache-2.0 license as published by
# the Apache Software Foundation, either version 2.0 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.

# You should have received a copy of the Apache-2.0 license
# along with this program. If not, see <https://www.apache.org/licenses/LICENSE-2.0>.
# For any questions about this software or licensing, please email
# opensource@seagate.com

import base64
import urllib.request
import urllib.error
import xml.dom.minidom
import ssl
import json
import hashlib
import sys
from warnings import warn

sys.tracebacklimit = 0


class BasicAuthLogin:
    '''
    A class to perform login operation using Base64 encoding
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : URL of login api 
    Methods
    -------
    __createHeader(): This function does Base64 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        '''
        '''
        self.__url = "%s://%s:%d/api/login/" % (self._protocol,
                                                ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does Base64 encoding of username and password provided by user
        :returns auth_string: Authentication key generated by Base64 encoding of username and password 
        '''
        temp_string = bytes(self.__username + ':' + self.__password, "utf-8")
        encodedBytes = base64.b64encode(temp_string)
        auth_string = str(encodedBytes, "utf-8")
        return auth_string

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response: Response is returned in XML format.
                         The content contains an OBJECT element. Within the OBJECT
                         element,a PROPERTY element with the "name" attribute of response
                         contains the "session key".
        :returns sessionKey: Session key generated after login of user
        '''
        xmlDoc = xml.dom.minidom.parseString(response.read())
        loginProps = xmlDoc.getElementsByTagName('PROPERTY')
        for lProp in loginProps:
            name = lProp.getAttribute('name')
            if name == 'response':
                self.__sessionKey = lProp.firstChild.data
        return self.__sessionKey

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after login of user
        '''
        self._set_host(self.__host)
        req = urllib.request.Request(self.__url)
        req.add_header('Authorization', 'Basic ' + self.__createHeader())
        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(self.__url)

        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey


class SHA256Login:

    '''
    A class to perform login operation using SHA256 encoding
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : url of login api 
    Methods
    -------
    __createHeader(): This function does SHA256 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        self.__tmpurl = "%s://%s:%d/api/login/" % (self._protocol,
                                                   ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does SHA256 encoding of username and password provided by user
        :returns : None
        '''
        userPass = bytes(self.__username + "_" + self.__password, "utf-8")
        m = hashlib.sha256()
        m.update(userPass)
        encoded = m.hexdigest()
        self.__url = self.__tmpurl + encoded

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response:Response returned in XML format.
                        The content contains an OBJECT element. Within the OBJECT
                        element,a PROPERTY element with the "name" attribute of response
                        contains the "session key".
        :returns sessionKey: Session key generated after login of user
        '''

        xmlDoc = xml.dom.minidom.parseString(response.read())
        loginProps = xmlDoc.getElementsByTagName('PROPERTY')

        for lProp in loginProps:
            name = lProp.getAttribute('name')
            if name == 'response':
                self.__sessionKey = lProp.firstChild.data

        return self.__sessionKey

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after successful login of user
        '''
        self._set_host(self.__host)
        self.__createHeader()
        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(self.__url, context=context)
        else:
            response = urllib.request.urlopen(self.__url)

        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey


class BasicAuthSHA256Login:

    '''
    A class to perform login operation using Base64+SHA256 encoding
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : url of login api 
    Methods
    -------
    __createHeader(): This function does Base64+SHA256 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        self.__tmpurl = "%s://%s:%d/api/login/" % (self._protocol,
                                                   ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does Base64+SHA256 encoding of username and password provided by user
        :returns auth_string: Authentication key generated by Base64 encoding of username and password 
        '''
        userPass = bytes(self.__username + "_" + self.__password, "utf-8")
        m = hashlib.sha256()
        m.update(userPass)
        encoded = m.hexdigest()
        self.__url = self.__tmpurl + encoded
        temp_string = bytes(self.__username + ':' + self.__password, "utf-8")
        encodedBytes = base64.b64encode(temp_string)
        auth_string = str(encodedBytes, "utf-8")
        return auth_string

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response:Response returned in XML format.
                        The content contains an OBJECT element. Within the OBJECT
                        element,a PROPERTY element with the "name" attribute of response
                        contains the "session key".
        :returns sessionKey: Session key generated after login of user
        '''

        xmlDoc = xml.dom.minidom.parseString(response.read())
        loginProps = xmlDoc.getElementsByTagName('PROPERTY')
        sessionKey = ''

        for lProp in loginProps:
            name = lProp.getAttribute('name')
            if name == 'response':
                self.__sessionKey = lProp.firstChild.data

        return self.__sessionKey

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after successful login of user
        '''
        self._set_host(self.__host)
        auth_string = self.__createHeader()
        req = urllib.request.Request(self.__url)
        req.add_header('Authorization', 'Basic ' + auth_string)
        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(req)
        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey


class RESTBasicAuthLogin:
    '''
    A class to perform login operation using Base64 encoding for REST Api
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : url of login api 
    Methods
    -------
    __createHeader(): This function does base64 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        self.__url = "%s://%s:%d/rest/v1/login/" % (self._protocol,
                                                    ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does Base64 encoding of username and password provided by user
        :returns auth_string: Authentication key generated by Base64 encoding of username and password 
        '''
        temp_string = bytes(self.__username + ':' + self.__password, "utf-8")
        encodedBytes = base64.b64encode(temp_string)
        auth_string = str(encodedBytes, "utf-8")
        return auth_string

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response: response of the request
        :returns sessionKey: Session key generated after login of user
        '''
        # print sessionKey
        cred = json.loads(response.read().decode('utf-8'))
        self.__sessionKey = cred['status'][0]['response']
        return self.__sessionKey

    def __showWarning(self):
        '''
        This function shows warning message as REST Api's are depracated
        '''
        warn("REST API's are deprecated.", category= Warning)
        warn("For best performance use API Login")

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after login of user
        '''
        self.__showWarning()
        self._set_host(self.__host)
        req = urllib.request.Request(self.__url)
        req.add_header('Authorization', 'Basic ' + self.__createHeader())
        req.add_header('dataType', 'json')

        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(req)
        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey


class RESTSHA256Login:
    '''
    A class to perform login operation using SHA256 encoding for REST Api
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : url of login api 
    Methods
    -------
    __createHeader(): This function does SHA256 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        self.__tmpurl = "%s://%s:%d/rest/v1/login/" % (self._protocol,
                                                       ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does SHA256 encoding of username and password provided by user
        :returns : None
        '''
        userPass = bytes(self.__username + "_" + self.__password, "utf-8")
        m = hashlib.sha256()
        m.update(userPass)
        encoded = m.hexdigest()
        self.__url = self.__tmpurl + encoded

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response: response of the request
        :returns sessionKey: Session key generated after login of user
        '''
        cred = json.loads(response.read().decode('utf-8'))
        self.__sessionKey = cred['status'][0]['response']
        return self.__sessionKey

    def __showWarning(self):
        '''
        This function shows warning message as REST Api's are depracated
        '''
        warn("REST API's are deprecated.", category= Warning)
        warn("For best performance use API Login")

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after login of user
        '''
        self.__showWarning()
        self._set_host(self.__host)
        self.__createHeader()
        req = urllib.request.Request(self.__url)
        req.add_header('dataType', 'json')

        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(req)
        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey


class RESTBasicAuthSHA256Login:
    '''
    A class to perform login operation using Base64+SHA256 encoding for REST api
    Attributes
    ----------
    __username : username of the user
    __password : password of the user
    __protocol : protocol to be followed for request (Http or Https)
    __host : Ip address of the array
    __port : port specified by the user
    __ssl_verify : Boolean value (True or False) for verification of SSL certificates
    __url : url of login api 
    Methods
    -------
    __createHeader(): This function does Base64+SHA256 encoding of username and password 
                        provided by user
    __getSessionKey(response): This function reads the response and gets session key  
    login() : This function creates and performs login request
    '''

    def __init__(self, username, password, host, port=443, protocol="https", ssl_verify=False):
        '''
        Constructs all the necessary attributes for the login request object
        :param username : username of the user
        :param password : password of the user
        :param protocol : protocol to be followed for request (Http or Https)
        :param host : Ip address of the array
        :param port : port specified by the user
        :param : ssl_verify : Boolean value (True or False) for verification of SSL certificates
        '''

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self._protocol = protocol
        self.__ssl_verify = ssl_verify
        self.__sessionKey = None

    def _set_host(self, ip_addr):
        self.__tmpurl = "%s://%s:%d/rest/v1/login/" % (self._protocol,
                                                       ip_addr, self.__port)

    def __createHeader(self):
        '''
        This function does Base64+SHA256 encoding of username and password provided by user
        :returns auth_string: Authentication key generated by Base64 encoding of username and password 
        '''
        userPass = bytes(self.__username + "_" + self.__password, "utf-8")
        m = hashlib.sha256()
        m.update(userPass)
        encoded = m.hexdigest()
        self.__url = self.__tmpurl + encoded
        temp_string = bytes(self.__username + ':' + self.__password, "utf-8")
        encodedBytes = base64.b64encode(temp_string)
        auth_string = str(encodedBytes, "utf-8")
        return auth_string

    def __getSessionKey(self, response):
        '''
        This function reads the response and gets session key  
        :param response: response of the request
        :returns sessionKey: Session key generated after login of user
        '''
        # print sessionKey
        cred = json.loads(response.read().decode('utf-8'))
        self.__sessionKey = cred['status'][0]['response']
        return self.__sessionKey

    def __showWarning(self):
        '''
        This function shows warning message as REST Api's are depracated
        '''
        warn("REST API's are deprecated.", category= Warning)
        warn("For best performance use API Login")

    def login(self):
        '''
        This function creates and performs login request
        :returns sessionKey: Session key generated after successful login of user
        '''
        self.__showWarning()
        self._set_host(self.__host)
        auth_string = self.__createHeader()
        req = urllib.request.Request(self.__url)
        req.add_header('Authorization', 'Basic ' + auth_string)
        req.add_header('dataType', 'json')

        if not self.__ssl_verify:
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(req)
        try:
            self.__sessionKey = self.__getSessionKey(response)
            if self.__sessionKey == "Authentication Unsuccessful":
                raise Exception("Authentication Unsuccessful")
            print("Logged in to array : ", self.__host)
        except urllib.error.HTTPError as HTTPError:
            print(HTTPError)
        except urllib.error.URLError as URLError:
            print(URLError)
        except Exception as err:
            print(err)
        return self.__sessionKey
