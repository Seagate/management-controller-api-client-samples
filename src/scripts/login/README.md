## Usage of scripts in this directory

### [login.py](./login/login.py)

It consumes the classes for login provided by loginFactory in python

- Introduction

  Depending upon the request and encoding type specified by user, it calls
  the respective class to perform login operation on the array.

- Usage

```
login.py [-h] -u USER -p PWD [-d] [-s] -i IP [-P PORT] [-x PROTOCOL] [-r {1,2}] [-e {1,2,3}]

required arguments:
  -u USER, --user USER  Username of MC (default: None)
  -p PWD, --pwd PWD     Password of specified user (default: None)
  -i IP, --ip IP        Enable Debug output (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable Debug output (default: False)
  -s, --ssl             Enable SSL verification (default: False)
  -P PORT, --port PORT  Specify the port (default: 443)
  -x PROTOCOL, --protocol PROTOCOL
                        Specify the protocol (default: https)
  -r {a,r}, --request {a,r}
                        Specify the request type: a for API, r for REST(depricated) (default: a)
  -e {b,s,bs}, --encoding {b,s,bs}
                        Specify the encoding type: b for base64, s for sha256, bs for base64+sha256 (default: b)
```
User needs to run login.py using python and pass the required parameters and optional parameters(if required).

```bash
python3 login/login.py -u username -p password -i 127.0.0.0
```
This prints:
```
Trying IP addresses 127.0.0.0 ...
Logging using API with BASE64 encoding
Logged in to array :  127.0.0.0
```
### [loginFactory.py](./login/loginFactory.py)

loginFactory provides classes for login procedure for XML API and REST API in python.

- Introduction

LoginFactory provides six classes out of which three are for XML API login and remaining are for REST login.

It consumes these classes

1. class BasicAuthLogin - A class to perform login operation using Base64 encoding for XML API
2. class SHA256Login - A class to perform login operation using SHA256 encoding for XML API
3. class BasicAuthSHA256Login - A class to perform login operation using Base64+SHA256 encoding for XML API
4. class RESTBasicAuthLogin - A class to perform login operation using Base64 encoding for REST
5. class RESTSHA256Login - A class to perform login operation using SHA256 encoding for REST
6. class RESTBasicAuthSHA256Login - A class to perform login operation using Base64+SHA256 encoding for REST

<b> DISCLAIMER :</b> <i>"REST endpoints are despricated. For best performance use API" </i>

- Usage

To perform login for XML API and Basic authentication with Base64 Encoding,
create object of Base64Login class and call login() method. It will return sessionKey
after successful login.

```python3
from loginFactory import BasicAuthLogin

obj1 = BasicAuthLogin("username", "password", "127.0.0.0")
sessionKey = obj1.login() 

obj2 = BasicAuthLogin("username", "password", "127.0.0.0", 443,"https", False)
sessionKey = obj2.login()
```
This prints:
```
Logged in to array :  127.0.0.0
```
If any mandatory parameter is not passed then it will throw error
```python3
from LoginFactory import BasicAuthLogin

obj = BasicAuthLogin("username", "127.0.0.0")
sessionKey = obj.login()
```
This prints:
```
Output: TypeError: __init__() missing 1 required positional argument 
```

If user passes invalid parameters then it will throw error as Authentication Unsuccessful
```python3
from LoginFactory import BasicAuthLogin

obj = BasicAuthLogin("username", "password@123", "127.0.0.0")
sessionKey = obj.login()
```
This prints:
```
Output: Authentication Unsuccessful
```

Parameters to be passed while creating object of Base64Login -

```
Mandatory parameters
	username    : Username of the user
	password    : Password of the user
	host        : IP address of the array
Optional parameters
 	port        : Port on which request should be sent
                      If not passed, by default port is set to 443.
	protocol    : Protocol to be followed for request (http or https)
		      If not passed, by default protocol is set to https.
	ssl_verify  : Boolean value (True or False) for verification of SSL certificates
		      If not passed, by default ssl_verify is set to False.
```

<b> NOTE :</b> <i>"Other Classes can be used in similar manner" </i>
