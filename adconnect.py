from ldap3 import Server, Connection, SAFE_SYNC, SUBTREE
import json, ast
server = Server('10.200.131.2',get_info='ALL')
conn = Connection(server, 'a_aivanov@test.local', '12345678', client_strategy=SAFE_SYNC, auto_bind=True)
# status, result, response, _ = conn.search('o=test', '(objectclass=*)')  # usually you don't need the original request (4th element of the returned tuple)
# conn.bind()
get_request=True
# print(conn.search('cn=Users,dc=test,dc=local','(&(objectCategory=User)(memberOf=cn=Domain Admins))',SUBTREE,attributes=['member']))
result = conn.search('cn=Users,dc=test,dc=local','(objectclass=person)')
for i in result[2]:
    i = str(i)
    # i = str(i)
    # i = i.replace("{'raw_dn': ",'[')
    print(ast.literal_eval(i))
    