from consumer import consum
import time
import csv
k = 0
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
        print(data)
    for i in data:
        if 'password' in i:
            print('Смена пароля   ')
            # del data[0]
        elif 'personal' in i:
            print('Создание изменение учетной записи   ')
            # del data[0]
        elif 'uuid' in i and len(i) == 1:
            print('блокировка учетки   ')
            # del data[0]
        elif 'name' in i and 'uuid' in i: 
            print('Создание изменение структуры   ')
            # del data[0]
        else:
            print('что-то')
        k += 1
    data = []
    if k == 1:
        s = False