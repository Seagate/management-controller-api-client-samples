# python3 p1.py -u manage -p Testit123! -i https://10.235.209.91
import sys

username = None
password = None
ip = None

def parse() :

    args = []
    for i in range(len(sys.argv)):
        args.append(sys.argv[i])
    if(len(args) == 7):
        username = args[2]
        password = args[4]
        ip = args[6]

        print(username + ' ' + password + ' ' + ip)
    else:
        if args.count("-u") == 0:
            print("Username is missing. Please provide username as -u USERNAME ")
        if args.count("-p") == 0:
            print("Password is missing. Please provide passord as -p PASSWORD ")
        if args.count("-i") == 0:
            print("IP address of array is missing. Please provide ip as -i IP ")
        showHelp()

def showHelp() :
    print('''
    Usage: ${0} [-h] [-u USERNAME] [-p PASSWORD] [-i IP]
    Description : Python script to access API using Basic Authentication with base64 encoding

    - Required Arguments:
        -u USERNAME,          Enter username
        -p PASSWORD,          Enter password
        -i IP,                Enter ip address of array
    - Optional Argument :
        -h,                   Show this help message and exit
    ''')
         

if __name__ == "__main__":
    parse()
