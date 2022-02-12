from curses.ascii import SUB
from ldap3 import Server, Connection, SAFE_SYNC, SUBTREE
import json, ast
server = Server('10.200.131.2',get_info='ALL')
conn = Connection(server, 'a_aivanov@test.local', '12345678', client_strategy=SAFE_SYNC, auto_bind=True)
get_request=True


# print(conn.search('dc=test,dc=local','(&(sAMAccountname=mpodturkin)(objectClass=User))'))


