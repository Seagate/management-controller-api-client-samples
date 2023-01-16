#!/usr/bin/python3

from main import MCClient
import logging as log
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

debug = False
extra_debug = False


def main():
    global port, password, username, debug, ip_addrs, protocol
    try:
        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-u", "--user", required = True, help="Username of MC")
        parser.add_argument("-p", "--pwd", required = True, help="Password of specified user")
        parser.add_argument("-d", "--debug", action="store_true", help="Enable Debug output")
        parser.add_argument("-s", "--ssl", action="store_true", help="Enable SSL verification")
        parser.add_argument("-i", "--ip", required = True, help="Enable Debug output")
        parser.add_argument("-P", "--port", type=int, default=443, help="Specify the port")
        parser.add_argument("-x", "--protocol", default="https", help="Specify the protocol")
        args = parser.parse_args()

        password = args.pwd
        username = args.user
        debug = args.debug
        ip_addrs = args.ip
        port = args.port
        protocol = args.protocol

    except Exception as e:
        log.exception('Exception in string format operation')
        

    if debug:
        log.getLogger().setLevel(log.DEBUG)

        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1

        log.getLogger("requests.packages.urllib3").setLevel(log.DEBUG)
        log.getLogger("requests.packages.urllib3").propagate = True
    else:
        log.getLogger().setLevel(log.INFO)

    print ("Trying IP addresses {} ...".format(ip_addrs))

    login(ip_addrs, username, password)

def login(ip_addrs,username,password):
    # Log in to the array
    if debug:
        print('password is %s' % password)
    client = MCClient(ip_addrs, username, password, protocol, port, False)
    client.login()

main()
