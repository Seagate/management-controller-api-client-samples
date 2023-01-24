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

from loginFactory import Base64Login, SHA256Login, Base64SHA256Login, RESTBase64Login, RESTSHA256Login, RESTBase64SHA256Login
import logging as log
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from const import RequestType, EncodingType


'''
A class to send login request on the basis of specified request_type and encoding_type.

Parameters
----------
username : username of the user
password : password of the user
protocol : protocol to be followed for request (Http or Https)
ip_addrs : Ip address of the array
port : port specified by the user
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
                EncodingType.BASE64.value: Base64Login(username, password, ip_addrs, port, protocol, ssl),
                EncodingType.SHA256.value: SHA256Login(username, password, ip_addrs, port, protocol, ssl),
                EncodingType.BASE64_SHA256.value: Base64SHA256Login(
                    username, password, ip_addrs, port, protocol, ssl)
            },
            RequestType.REST.value: {
                EncodingType.BASE64.value: RESTBase64Login(username, password, ip_addrs, port, protocol, ssl),
                EncodingType.SHA256.value: RESTSHA256Login(username, password, ip_addrs, port, protocol, ssl),
                EncodingType.BASE64_SHA256.value: RESTBase64SHA256Login(
                    username, password, ip_addrs, port, protocol, ssl)
            }
        }
        try:
            # Reading request_type and encoding_type for logging
            client = request_encoding_keys[request][encoding]
            print("Logging using", RequestType(request).name,
                  "with", EncodingType(encoding).name, "encoding")
            client.login()
        except Exception as e:
            print('ERROR: %s' % e)
        return


def main():
    global username, password, ip_addrs, debug, ssl, port, protocol, request, encoding
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
                            "b", "s", "bs"], help="Specify the encoding type: b for base64, s for sha256, bs for base64+sha256")
        args = parser.parse_args()

        password = args.pwd
        username = args.user
        debug = args.debug
        ip_addrs = args.ip
        port = args.port
        protocol = args.protocol
        ssl = args.ssl
        request = args.request
        encoding = args.encoding

    except Exception as e:
        print('ERROR: %s' %e)

    if debug:
        log.getLogger().setLevel(log.DEBUG)
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
        log.getLogger("requests.packages.urllib3").setLevel(log.DEBUG)
        log.getLogger("requests.packages.urllib3").propagate = True
    else:
        log.getLogger().setLevel(log.INFO)

    print("Trying IP addresses {} ...".format(ip_addrs))
    Login().login()


main()
