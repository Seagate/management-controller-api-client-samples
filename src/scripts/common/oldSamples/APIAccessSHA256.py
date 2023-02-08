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