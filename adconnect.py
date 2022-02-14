from curses.ascii import SUB
from ldap3 import Server, Connection, SAFE_SYNC, SUBTREE
import json, ast
import settings
server = Server('10.200.131.2',get_info='ALL')
conn = Connection(server, settings.dlogin, settings.dpass, client_strategy=SAFE_SYNC, auto_bind=True)
get_request=True

# name = 'Исматуллаев Амир Хондамирович'
# result = conn.search('dc=test,dc=local',f'(&(ncfuGUID=15F7D27F-BDC2-40DE-9546-2EFB3218191F)(objectClass=User))')
# resultname = result[2]
# for i in result:
#     print(i)
#     print('*'*20)
# resultname = resultname[0]

# print(resultname['dn'])

