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

import logging as log
from http.client import HTTPConnection
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from loginFactory import Base64Login, SHA256Login, Base64SHA256Login, RESTBase64Login, RESTSHA256Login, RESTBase64SHA256Login
from const import RequestType, EncodingType


'''
A class to send login request on the basis of specified request_type and encoding_type.

Parameters
----------
USERNAME : username of the user
PASSWORD : password of the user
PROTOCOL : protocol to be followed for request (Http or Https)
IP_ADDRS : Ip address of the array
PORT : port specified by the user
ssl_verify : Boolean value (True or False) for verification of SSL certificates

Methods
-------
login() : This function sends login request
'''


class Login:
    '''
    This function sends login request

    :returns None

    '''
    @staticmethod
    def login():
        '''
        request_encoding_keys: Two Level nested map
        First Level Storage : API / REST
        Inner Level(leaf) backend : BASE64 / SHA256 / BASE64+SHA256
        '''
        request_encoding_keys = {
            RequestType.API.value: {
                EncodingType.BASE64.value: Base64Login(USERNAME, PASSWORD, IP_ADDRS,
                    PORT, PROTOCOL, SSL),
                EncodingType.SHA256.value: SHA256Login(USERNAME, PASSWORD, IP_ADDRS,
                    PORT, PROTOCOL, SSL),
                EncodingType.BASE64_SHA256.value: Base64SHA256Login(
                    USERNAME, PASSWORD, IP_ADDRS, PORT, PROTOCOL, SSL)
            },
            RequestType.REST.value: {
                EncodingType.BASE64.value: RESTBase64Login(USERNAME, PASSWORD, IP_ADDRS,
                    PORT, PROTOCOL, SSL),
                EncodingType.SHA256.value: RESTSHA256Login(USERNAME, PASSWORD, IP_ADDRS,
                    PORT, PROTOCOL, SSL),
                EncodingType.BASE64_SHA256.value: RESTBase64SHA256Login(
                    USERNAME, PASSWORD, IP_ADDRS, PORT, PROTOCOL, SSL)
            }
        }
        try:
            # Reading request_type and encoding_type for logging
            client = request_encoding_keys[REQUEST][ENCODING]
            print("Logging using", RequestType(REQUEST).name,
                  "with", EncodingType(ENCODING).name, "encoding")
            client.login()
        except Exception as exp:
            print('ERROR: %s' % exp)


def main():
    global USERNAME, PASSWORD, IP_ADDRS, DEBUG, SSL, PORT, PROTOCOL, REQUEST, ENCODING
    try:
        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-u", "--user", required=True,
                            help="Username of MC")
        parser.add_argument("-p", "--pwd", required=True,
                            help="Password of specified user")
        parser.add_argument(
            "-d", "--debug", action="store_true", help="Enable Debug output")
        parser.add_argument("-s", "--ssl", action="store_true",
                            help="Enable SSL verification")
        parser.add_argument("-i", "--ip", required=True,
                            help="Enable Debug output")
        parser.add_argument("-P", "--port", type=int,
                            default=443, help="Specify the port")
        parser.add_argument("-x", "--protocol",
                            default="https", help="Specify the protocol")
        parser.add_argument("-r", "--request", default="a", choices=[
                            "a", "r"], help="Specify the request type: a for API, r for REST")
        parser.add_argument("-e", "--encoding", default="b", choices=[
                            "b", "s", "bs"], help="Specify the encoding type: b for base64,s for sha256, bs for base64+sha256")
        args = parser.parse_args()

        PASSWORD = args.pwd
        USERNAME = args.user
        DEBUG = args.debug
        IP_ADDRS = args.ip
        PORT = args.port
        PROTOCOL = args.protocol
        SSL = args.ssl
        REQUEST = args.request
        ENCODING = args.encoding

    except Exception as exp:
        print('ERROR: %s' %exp)

    if DEBUG:
        log.getLogger().setLevel(log.DEBUG)
        HTTPConnection.debuglevel = 1
        log.getLogger("requests.packages.urllib3").setLevel(log.DEBUG)
        log.getLogger("requests.packages.urllib3").propagate = True
    else:
        log.getLogger().setLevel(log.INFO)

    print("Trying IP addresses {} ...".format(IP_ADDRS))
    Login().login()


main()
