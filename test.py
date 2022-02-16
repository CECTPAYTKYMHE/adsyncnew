import json,ast
name1 = b'{"id":"0046DC80-7487-4664-A5F9-A6227256E18D","positions":[],"study":[],"roles":["Student"],"personal":{"lastName":"\xd0\xa1\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb4\xd1\x83\xd1\x85\xd0\xb8\xd0\xbd\xd0\xb0                                                                                ","firstName":"\xd0\x95\xd0\xbb\xd0\xb8\xd0\xb7\xd0\xb0\xd0\xb2\xd0\xb5\xd1\x82\xd0\xb0                                                             ","middleName":"\xd0\x94\xd0\xbc\xd0\xb8\xd1\x82\xd1\x80\xd0\xb8\xd0\xb5\xd0\xb2\xd0\xbd\xd0\xb0                                                            ","gender":false}}'
name2 = b'{"id":"B7E14821-044D-4450-873F-067B52531F71","positions":[{"code":"1815810","orgId":"5E31EF25-DF6A-48F3-BF63-F73160E7F96C","positionName":"\xd0\xbb\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x80\xd0\xb0\xd0\xbd\xd1\x82","positionType":"\xd0\x9e\xd0\x9c\xd0\xa0"}],"study":[],"roles":["Employee","Manager"],"personal":{"lastName":"\xd0\x9d\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xb5\xd0\xb2","firstName":"\xd0\x90\xd0\xb9\xd0\xb4\xd0\xb5\xd0\xbc\xd0\xb8\xd1\x80","middleName":"\xd0\x9c\xd1\x83\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd0\xb2\xd0\xb8\xd1\x87","gender":true}}'
name3 = b'{"id":"7E7F92D8-6424-43B6-9CF5-6A7D2273D50F","positions":[{"code":"1815934","orgId":"F0631FFE-40A7-49F3-B9F8-B4ECFEE73133","positionName":"\xd0\xbb\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x80\xd0\xb0\xd0\xbd\xd1\x82","positionType":"\xd0\x9e\xd0\x9c\xd0\xa0"}],"study":[{"code":"1613504","orgId":"1FDE30DB-16C2-47C4-B9CA-ED4503EB2138","academicGroup":"\xd0\xa5\xd0\x98\xd0\x9c-\xd0\xb1-\xd0\xbe-18-1","academicGroupUuid":"D18D667C-73EF-47DD-B825-F648300CE9AC","specialityCode":"04.03.01"}],"roles":["Employee","Manager","Student"],"personal":{"lastName":"\xd0\x91\xd0\xbe\xd0\xb1\xd1\x80\xd0\xbe\xd0\xb2","firstName":"\xd0\x90\xd0\xbd\xd0\xb0\xd1\x82\xd0\xbe\xd0\xbb\xd0\xb8\xd0\xb9","middleName":"\xd0\x90\xd0\xbd\xd0\xb0\xd1\x82\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb5\xd0\xb2\xd0\xb8\xd1\x87","gender":true}}'
name2 = json.loads(name2)
print(name2['positions'][0])

print(name2['study'])

print(type(name2['study']))
if not name2['study']:
    print(True)