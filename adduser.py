'''
@author: aivanov
'''
from asyncio import start_unix_server
import ldap3
from ldap3 import MODIFY_REPLACE, MODIFY_DELETE
import adconnect
import settings
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups as removeUsersFromGroups
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
    def __init__(self,givenName,sn,middleName,ncfuGUID,group,position,study):
        self.__conn = adconnect.conn
        self.__givenName = givenName.replace(' ','')
        self.__middleName = middleName.replace(' ','')
        self.__group = group
        self.__sn = sn.replace(' ','')
        if self.__group != []:
            self.__uac = '544'
        else:
            self.__uac = '546'
        self.__position = position
        self.__study = study
        self.__employeeNumber = ncfuGUID.replace('-','')
        self.__ncfuGUID = ncfuGUID
        self.checkmiddlenameexist()
        self.logingenerator()
        self.dngeneratorfornewuser()
        self.getinitials()
        self.checkdeptitle()
        self.addmodifyuser()
        # self.userresultfortest()
        
    # Проверям наличие места работы, группы студента, пишем '-' если ничего не найдено
    # '-' потом проверяются в addmodifyuser() если они есть оставляют поле пустым(удаляют старые атрибуты)
    def checkdeptitle(self):
        if self.__study == []:
            self.__title = '-'
            self.__department = '-'
        else:
            self.__title = self.__study[0]['academicGroup']
            self.__department = self.__study[0]['specialityCode']
        if self.__position == []:
            pass
        else:
            self.__title = self.__position[0]['positionName']
            self.__department = self.__position[0]['positionType']
        return self.__department,self.__title
        
            
    # Проверка на наличие отчества, если отчества нету то инициалы только имени. 
    def getinitials(self):
        if self.__givenName != '' and self.__middleName != '<not set>':
            self.__initials = f'{self.__givenName[0:1]}.{self.__middleName[0:1]}.'
        else:
            self.__initials = f'{self.__givenName[0:1]}.'
        return self.__initials
    
    # Проверка на CN в домене
    def cnisexist(self):
        __iscnexist = self.__conn.search({settings.dndomian},f'(&(cn={self.__fullname})(objectClass=User))')
        __iscnexist = str(__iscnexist)
        if 'raw_dn' in __iscnexist:
            return True
        else:
            return False
        
    # Если такой CN уже существует то добавлять _[1-...] пока не будет совпадения
    def ifcnexist(self):
        i = 0
        while self.cnisexist():
            i+=1
            name = f'{self.__fullname}_{i}'
            namexist= self.__conn.search({settings.dndomian},f'(&(cn={name})(objectClass=User))')
            namexist = str(namexist)
            if 'raw_dn' in namexist:
                del name
            else:
                self.__fullname = name
        return self.__fullname
    
    # Проверка существования пользователя на основании ncfuGUID
    def usernotexist(self):
        __userexist = self.__conn.search({settings.dndomian},f'(&(ncfuGUID={self.__ncfuGUID})(objectClass=User))')
        __userexist = str(__userexist)
        if 'raw_dn' in __userexist:
            return False
        else:
            return True

    # Генерация логина пользователя с проверкой существующих, если существует
    # то добавлять по одной букве с максимальным количеством 3, если и такой существует то 
    # добавлять цифры в конце логина
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
        
    # Проверка наличия отчества, с возвратом CN, должен стоять первым в инит класса!
    def checkmiddlenameexist(self):
        if self.__middleName != '':
            self.__fullname = f'{self.__sn} {self.__givenName} {self.__middleName}'
        else:
            self.__fullname = f'{self.__sn} {self.__givenName}'
            self.__middleName = '<not set>'
        self.__displayname = self.__fullname
        return self.__fullname
            
    # Генерация DN для нового пользователя должен стоять после ifcnexist
    def dngeneratorfornewuser(self):
        self.__dn = f'cn={self.__fullname},ou={self.__sn[0:1]},ou=Пользователи,{settings.dndomian}'
        return self.__dn
    
    # Генерация DN для существующего пользователя на основании ncfuGUID 
    # вытягиваем DN из возвращенного словаря
    def dngeneratorforexistuser(self):
        __userexist = self.__conn.search('dc=test,dc=local',f'(&(ncfuGUID={self.__ncfuGUID})(objectClass=User))')
        __userexist = __userexist[2][0]['dn']
        self.__dn = __userexist
        return self.__dn
    
    # Вызов создания, изменения пользователей
    def addmodifyuser(self):
        if self.usernotexist():
            print('Создание учетной записи', self.__displayname,self.__group)
            self.ifcnexist()
            self.dngeneratorfornewuser()
            self.adduser()
        else:
            print('Изменение учетной записи', self.__displayname,self.__group)
            self.ifcnexist()
            self.dngeneratorforexistuser()
            self.modifyuser()
            
    
    def userresultfortest(self):
        if self.usernotexist():
            print('New user')
            self.ifcnexist()
            self.dngeneratorfornewuser()
        else:
            print('Modify user')
            self.ifcnexist()
            self.dngeneratorforexistuser()
        print(f'\
                dn: {self.__dn}\n\
                sn: {self.__sn}\n\
                givenName : {self.__givenName}\n\
                middleName: {self.__middleName}\n\
                ncfuFullName: {self.__displayname}\n\
                ncfuTimestamp: {settings.time}\n\
                userAccountControl: {self.__uac}\n\
                employeeNumber: {self.__employeeNumber}\n\
                initials: {self.__initials}\n\
                displayName: {self.__displayname}\n\
                userPrincipalName: {self.__sAMA}{settings.domain}\n\
                sAMAccountName : {self.__sAMA}\n\
                ncfuGUID: {self.__ncfuGUID}\n\
                group : {self.__group}\n')
                
    # Создание нового пользователя, добавление пользователя в группы.  
    def adduser(self):
        self.__conn.add(f'{self.__dn}', ['person','user'],
            {'givenName' : {self.__givenName},
            'sn': {self.__sn},
            'ncfuFullName': {self.__displayname},
            'ncfuTimestamp': {settings.time},
            'userAccountControl': {self.__uac},
            'employeeNumber': {self.__employeeNumber},
            'initials': {self.__initials},
            'middleName': {self.__middleName},
            'displayName': {self.__displayname},
            'userPrincipalName': f'{self.__sAMA}{settings.domain}',
            'sAMAccountName' : {self.__sAMA},
            'ncfuGUID': {self.__ncfuGUID},
            })
        if self.__title == '-' or self.__department == '-':
            self.__conn.modify(self.__dn,
                               {
                                'title': [(MODIFY_DELETE, [])],
                                'department': [(MODIFY_DELETE, [])]
                               })
        else:
            self.__conn.modify(self.__dn,
                               {
                                'title': [(MODIFY_REPLACE, [self.__title])],
                                'department': [(MODIFY_REPLACE, [self.__department])]
                               })
        #print(self.__conn.result)
        if self.__group != '':
            for group in self.__group:
                addUsersInGroups(self.__conn,{self.__dn},f'cn={group},ou=Пользователи,{settings.dndomian}')
                #print(self.__conn.result)
    
    # Изменение ползователей, удаляем пользователя из стандартным групп, 
    # добавляем пришедшие группы, вносим изменения в пользователя.
    def modifyuser(self):
        for group in settings.defaultgroup:
            removeUsersFromGroups(self.__conn,{self.__dn},f'cn={group},ou=Пользователи,{settings.dndomian}',fix=True)
            #print(self.__conn.result)
        if self.__group != '':
            for group in self.__group:
                if group in settings.defaultgroup:
                    addUsersInGroups(self.__conn,{self.__dn},f'cn={group},ou=Пользователи,{settings.dndomian}')
                    #print(self.__conn.result)
        self.__conn.modify(self.__dn,\
            {'givenName' : [(MODIFY_REPLACE, [self.__givenName])],
            'sn': [(MODIFY_REPLACE, [self.__sn])],
            'middleName': [(MODIFY_REPLACE, [self.__middleName])],
            'displayName': [(MODIFY_REPLACE, [self.__displayname])],
            'ncfuFullName': [(MODIFY_REPLACE, [self.__displayname])],
            'userAccountControl': [(MODIFY_REPLACE, [self.__uac])],
            'initials': [(MODIFY_REPLACE, [self.__initials])],
            'ncfuTimestamp': [(MODIFY_REPLACE, [settings.time])]
            })
        if self.__title == '-' or self.__department == '-':
            self.__conn.modify(self.__dn,
                               {
                                'title': [(MODIFY_DELETE, [])],
                                'department': [(MODIFY_DELETE, [])]
                               })
        else:
            self.__conn.modify(self.__dn,
                               {
                                'title': [(MODIFY_REPLACE, [self.__title])],
                                'department': [(MODIFY_REPLACE, [self.__department])]
                               })
        #print(self.__conn.result)
        self.__conn.modify_dn(self.__dn,f'cn={self.__displayname}',new_superior=f'ou={self.__sn[0:1]},ou=Пользователи,{settings.dndomian}')
        #print(self.__conn.result)



if __name__ == '__main__':
    test = User('Елизавета','Солодухина','Дмитриевна','0046DC80-7487-4664-A5F9-A6227256E18D',['Chair','Manager','Student','Employee'],[],[])
    
    