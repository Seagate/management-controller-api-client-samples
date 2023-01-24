import hashlib
import sys
import urllib.request
import xml.dom.minidom
import ssl

ip = sys.argv[1]

userPass = bytes('manage_Testit123!', "utf-8")
m = hashlib.sha256()
m.update(userPass)
encoded = m.hexdigest()
print("SHA256 = " + encoded + "\n")
url = ip + '/api/login/' + encoded

# Skip certificate verification
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url, context=context)
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