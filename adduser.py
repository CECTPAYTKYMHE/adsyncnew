# -*- coding: utf-8 -*-
'''
@author: aivanov
'''
import ldap3
import adconnect
import settings
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from translit_gost_R_52535_1 import translit
from ldap3.utils.log import set_library_log_detail_level, OFF, BASIC, NETWORK, EXTENDED
set_library_log_detail_level(EXTENDED)
class User:
    # Инициалиация класса пользователя, выдача UAC(если tuple групп пустой, то блокировать учетную запись)
    # Проверка наличия отчества
    # Генерация логина(с проверкой существующих в домене)
    # Генерация DN и CN пользователя(с проверкой существующих в домене)
    # Генерация инициалов
    # Создание изменение пользователя и его групп
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
        # self.addmodifyuser()
        self.userresultfortest()
        
        
    def getinitials(self):
        if self.__givenName != '' and self.__middleName != '<not set>':
            self.__initials = f'{self.__givenName[0:1]}.{self.__middleName[0:1]}.'
        else:
            self.__initials = f'{self.__givenName[0:1]}.'
        return self.__initials
    
    def cnisexist(self):
        __iscnexist = self.__conn.search({settings.dndomian},f'(&(cn={self.__displayName})(objectClass=User))')
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
            namexist= self.__conn.search({settings.dndomian},f'(&(cn={name})(objectClass=User))')
            namexist = str(namexist)
            if 'raw_dn' in namexist:
                del name
            else:
                self.__displayName = name
        return self.__displayName
        
    def usernotexist(self):
        __userexist = self.__conn.search({settings.dndomian},f'(&(ncfuGUID={self.__ncfuGUID})(objectClass=User))')
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
            __isloginexist = self.__conn.search({settings.dndomian},f'(&(sAMAccountname={self.__sAMA})(objectClass=User))')
            __isloginexist = str(__isloginexist)
            if 'raw_dn' in __isloginexist and i <= 3:
                i += 1
            elif 'raw_dn' not in __isloginexist:
                return self.__sAMA
            else:
                islogin = False
        islogin = True
        while islogin:
            k += 1
            login = f'{self.__sAMA}{k}'
            __isloginexist = self.__conn.search({settings.dndomian},f'(&(sAMAccountname={login})(objectClass=User))')
            __isloginexist = str(__isloginexist)
            if 'raw_dn' in __isloginexist and i >= 3:
                del login
            else:
                self.__sAMA = login
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
        self.__dn = f'cn={self.__displayName},ou={self.__sn[0:1]},ou=Пользователи,{settings.dndomian}'
        return self.__dn
    
    def addmodifyuser(self):
        if self.usernotexist():
            self.ifcnexist()
            self.dngenerator()
            self.adduser()
        else:
            self.ifcnexist()
            self.dngenerator()
            print(self.__displayName)
            print('User exist')
    
    def userresultfortest(self):
        print(f'\
                sn: {self.__sn}\n\
                givenName : {self.__givenName}\n\
                middleName: {self.__middleName}\n\
                ncfuFullName: {self.__displayName}\n\
                ncfuTimestamp: {settings.time}\n\
                userAccountControl: {self.__uac}\n\
                employeeNumber: {self.__employeeNumber}\n\
                initials: {self.__initials}\n\
                displayName: {self.__displayName}\n\
                userPrincipalName: {self.__sAMA}{settings.domain}\n\
                sAMAccountName : {self.__sAMA}\n\
                ncfuGUID: {self.__ncfuGUID}\n\
                group : {self.__group}\n')
                
        
    def adduser(self):
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
                
    def modifyuser(self):
        pass
        
           


# test = User('Амир','Исматуллаев','Васильевич','8B22574D-jfdjfldskfods333434234443',['Student','Chair','Manager','Employee'])
