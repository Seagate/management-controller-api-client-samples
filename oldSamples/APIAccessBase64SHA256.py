import base64
import hashlib
import sys
import urllib.request
import xml.dom.minidom
import ssl

username = 'manage'
password = 'Testit123!'

if sys.argv[1]:
    ip = sys.argv[1]
else:
    sys.exit(1)

# Base64 encoding
temp_string = bytes(username + ':' + password, "utf-8")
encodedBytes = base64.b64encode(temp_string)
auth_string = str(encodedBytes, "utf-8")
print("Base64 = " + auth_string + "\n")

# Generate SHA256
userPass = bytes(username + '_' + password, "utf-8")
m = hashlib.sha256()
m.update(userPass)
encoded = m.hexdigest()
print("SHA256 = " + encoded + "\n")

url = ip + '/api/login/' + encoded

req = urllib.request.Request(url)
req.add_header('Authorization', 'Basic ' + auth_string)

print(req.get_full_url())
print(req.get_header('Authorization'))

# Skip certificate verification
context = ssl._create_unverified_context()
response = urllib.request.urlopen(req, context=context)
xmlDoc = xml.dom.minidom.parseString(response.read())
loginObjs = xmlDoc.getElementsByTagName('OBJECT')
loginProps = xmlDoc.getElementsByTagName('PROPERTY')
sessionKey = ''

for lProp in loginProps:
    name = lProp.getAttribute('name')
    print("Property = " + name)
    if name == 'response':
        sessionKey = lProp.firstChild.data

print("Session Key = " + sessionKey + "\n" )

url = ip + '/api/show/disks'
req = urllib.request.Request(url)
req.add_header('sessionKey', sessionKey)
req.add_header('dataType', 'console')
response = urllib.request.urlopen(req, context=context)
print(response.read().decode('utf-8'))
