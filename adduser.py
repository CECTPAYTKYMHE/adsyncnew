import ldap3
import adconnect
import settings
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from transliterate import translit
from ldap3.utils.log import set_library_log_detail_level, OFF, BASIC, NETWORK, EXTENDED
set_library_log_detail_level(EXTENDED)
class User:
    def __init__(self,givenName,sn,middleName,ncfuGUID,group):
        self.__conn = adconnect.conn
        self.__givenName = givenName.replace(' ','')
        self.__middleName = middleName.replace(' ','')
        self.__group = group
        self.__sn = sn.replace(' ','')
        if self.__group != '':
            self.__uac = '544'
        else:
            self.__uac = '546'
        self.__employeeNumber = ncfuGUID.replace('-','')
        self.__ncfuGUID = ncfuGUID
        self.checkmiddlenameexist()
        self.logingenerator()
        self.dngenerator()
        self.getinitials()
        self.adduser()
        
        
    def getinitials(self):
        if self.__givenName != '' and self.__middleName != '<not set>':
            self.__initials = f'{self.__givenName[0:1]}.{self.__middleName[0:1]}.'
        else:
            self.__initials = f'{self.__givenName[0:1]}.'
        return self.__initials
    
    def cnisexist(self):
        __iscnexist = self.__conn.search('dc=test,dc=local',f'(&(cn={self.__displayName})(objectClass=User))')
        __iscnexist = str(__iscnexist)
        if 'raw_dn' in __iscnexist:
            return True
        else:
            return False
    
    def ifcnexist(self):
        i = 0
        while self.cnisexist():
            i+=1
            name = f'{self.__displayName}_{i}'
            namexist= self.__conn.search('dc=test,dc=local',f'(&(cn={name})(objectClass=User))')
            namexist = str(namexist)
            if 'raw_dn' in namexist:
                del name
            else:
                self.__displayName = name
        return self.__displayName
        
    def usernotexist(self):
        __userexist = self.__conn.search('dc=test,dc=local',f'(&(ncfuGUID={self.__ncfuGUID})(objectClass=User))')
        __userexist = str(__userexist)
        if 'raw_dn' in __userexist:
            return False
        else:
            return True
        
    def logingenerator(self):
        islogin = True
        i = 1
        k = 0
        firstpart = translit(self.__givenName, language_code='ru', reversed=True)
        lastpart = translit(self.__sn, language_code='ru', reversed=True)
        while islogin:
            self.__sAMA = firstpart[0:i] + lastpart
            self.__sAMA = self.__sAMA.lower()
            __isloginexist = self.__conn.search('dc=test,dc=local',f'(&(sAMAccountname={self.__sAMA})(objectClass=User))')
            __isloginexist = str(__isloginexist)
            if 'raw_dn' in __isloginexist:
                i += 1
                if i >= 3:
                    self.__sAMA = f'{self.__sAMA}{k}'
                    k += 1
            else:
                islogin = False
                return self.__sAMA
    
    def checkmiddlenameexist(self):
        if self.__middleName != '':
            self.__displayName = f'{self.__sn} {self.__givenName} {self.__middleName}'
        else:
            self.__displayName = f'{self.__sn} {self.__givenName}'
            self.__middleName = '<not set>'

        return self.__displayName
            
           
    def dngenerator(self):
        self.__dn = f'cn={self.__displayName},ou={self.__sn[0:1]},ou=Пользователи,dc=test,dc=local'
        return self.__dn
        
    def adduser(self):
        if self.usernotexist():
            self.ifcnexist()
            self.dngenerator()
            self.__conn.add(f'{self.__dn}', ['person','user'],
        {'givenName' : {self.__givenName},
        'sn': {self.__sn},
        'ncfuFullName': {self.__displayName},
        'ncfuTimestamp': {settings.time},
        'userAccountControl': {self.__uac},
        'employeeNumber': {self.__employeeNumber},
        'initials': {self.__initials},
        'middleName': {self.__middleName},
        'displayName': {self.__displayName},
        'userPrincipalName': f'{self.__sAMA}{settings.domain}',
        'sAMAccountName' : {self.__sAMA},
        'ncfuGUID': {self.__ncfuGUID}})
            print(self.__conn.result)
            if self.__group != '':
                for group in self.__group:
                    addUsersInGroups(self.__conn,{self.__dn},f'cn={group},ou=Пользователи,dc=test,dc=local')
                print(self.__conn.result)
        else:
            self.ifcnexist()
            self.dngenerator()
            print(self.__displayName)
            

            
                

test = User('Амир','Исматуллаев','  ','8B22574D-jfdjfldskfods333434233',['Student'])
print(test.__dict__)
print(test.usernotexist())
