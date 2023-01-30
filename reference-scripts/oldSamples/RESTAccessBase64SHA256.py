import base64
import hashlib
import json
import urllib.request
import sys
import ssl

username = 'manage'
password = 'Testit123!'

if sys.argv[1]:
    ip = sys.argv[1]
else:
    sys.exit(1)

# Generate SHA256
userPass = bytes(username + '_' + password, "utf-8")
m = hashlib.sha256()
m.update(userPass)
encoded = m.hexdigest()
print("SHA256 = " + encoded + "\n")
temp_string = bytes(username + ':' + password, "utf-8")
encodedBytes = base64.b64encode(temp_string)
auth_string = str(encodedBytes, "utf-8")
print("Base64 = " + auth_string + "\n")
url = ip + '/rest/v1/login/' + encoded

req = urllib.request.Request(url)
req.add_header('Authorization', 'Basic ' + auth_string)
req.add_header('dataType', 'json')
print(req.get_full_url())
print(req.get_header('Authorization'))

# Skip certificate verification
context = ssl._create_unverified_context()
response = urllib.request.urlopen(req, context=context)

# print sessionKey
print(response.info())
cred = json.loads(response.read().decode('utf-8'))
sessionKey = cred['status'][0]['response']
url = ip + '/rest/v1/drives'
req = urllib.request.Request(url)
req.add_header('sessionKey', sessionKey)
req.add_header('dataType', 'json')
response = urllib.request.urlopen(req, context=context)

# print data
print(response.read().decode('utf-8'))