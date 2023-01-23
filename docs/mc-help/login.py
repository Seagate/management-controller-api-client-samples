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

from loginFactory import MCClient
import logging as log
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class Login:
    '''
    Send login request on the basis of specified request_type and encryption_type. 
    '''
    @staticmethod
    def login():
        '''
        request_encryption_keys: Two Level nested map
        First Level Storage : API / REST
        Inner Level(leaf) backend : BASE64 / SHA256 / BASE64+SHA256
        :returns: None
        '''
        request_encryption_keys = {
            "api": {
                "base64": MCClient(ip_addrs, username, password, protocol, port, ssl),
                "sha256": MCClient(ip_addrs, username, password, protocol, port, ssl),
                "base64+sha256": MCClient(ip_addrs, username, password, protocol, port, ssl)
            },
            "rest": {
                "base64": MCClient(ip_addrs, username, password, protocol, port, ssl),
                "sha256": MCClient(ip_addrs, username, password, protocol, port, ssl),
                "base64+sha256": MCClient(ip_addrs, username, password, protocol, port, ssl)
            }
        }
        try:
            # Reading request_type and encryption_type for logging
            client = request_encryption_keys[request][encrytion]
            print("Logging using", request, "with", encrytion, "encryption")
            client.login()
        except Exception as e:
            print('ERROR: %s' % e)
        return


def usage():
    print('usage: [-h] -u USER -p PWD [-d] [-s] -i IP [-P PORT] [-x PROTOCOL]')
    print(' Arguments: ')
    print('   -h              show this help message and exit')
    print('   -u USER         Username of MC (default: None)')
    print('   -p PWD          Password of specified user (default: None)')
    print('   -d              Enable Debug output (default: False)')
    print('   -s              Enable SSL verification (default: False)')
    print('   -i IP           Enable Debug output (default: None)')
    print('   -P PORT         Specify the port (default: 443)')
    print('   -x PROTOCOL     Specify the protocol (default: https)')
    print('   -r TYPE         Specify the type of request(API/REST) (default: API)')
    print('   -e ENCRYPTION   Specify encryption type(base64/sha256/base64+sha256) (default: base64)')


def main():
    global username, password, ip_addrs, debug, ssl, port, protocol, request, encrytion
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
        parser.add_argument("-r", "--request", default="api",
                            choices=["api", "rest"], help="Specify the type of request")
        parser.add_argument("-e", "--encryption", default="base64", choices=[
                            "base64", "sha256", "base64+sha256"], help="Specify encryption type")
        args = parser.parse_args()

        password = args.pwd
        username = args.user
        debug = args.debug
        ip_addrs = args.ip
        port = args.port
        protocol = args.protocol
        ssl = args.ssl
        request = args.request
        encrytion = args.encryption

    except Exception as e:
        usage()
        print('ERROR: %s' % e)

    if debug:
        log.getLogger().setLevel(log.DEBUG)
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
        log.getLogger("requests.packages.urllib3").setLevel(log.DEBUG)
        log.getLogger("requests.packages.urllib3").propagate = True
    else:
        log.getLogger().setLevel(log.INFO)

    print("Trying IP addresses {} ...".format(ip_addrs))
    obj = Login()
    obj.login()


main()
