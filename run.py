from consumer import consum
import time
import csv
import settings
import adduser
k = 1
s = True
# k = []
# data = []
# adduser = Consumer()
# consumer()
# data = consumer.data
# print(data)
data = []
while s:
    if len(data) == 0:

        data = consum()
        # print(data)
    for i in data:
        if 'password' in i:
            print('Смена пароля   ')
            # del data[0]
        elif 'personal' in i:
            adduser.User(\
                i['personal']['firstName'],\
                i['personal']['lastName'],\
                i['personal']['middleName'],\
                i['id'],\
                i['roles'])
            print('Создание изменение учетной записи   ',\
                i['personal']['firstName'],\
                i['personal']['lastName'],\
                i['personal']['middleName'],\
                i['id'],\
                ''.join(i['roles']))
            print(adduser.User.__dict__)
            # del data[0]
        elif 'uuid' in i and len(i) == 1:
            print('блокировка учетки   ')
            # del data[0]
        elif 'name' in i and 'uuid' in i: 
            print('Создание изменение структуры   ')
            # del data[0]
        else:
            print('что-то')
    # k += 1
    data = []
    if len(data) == 0:
        s = False