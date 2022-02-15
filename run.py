# from consumer import consum
import time
import csv

import settings
import adduser
k = 1
s = True
# data = []
def main(data):
    k = 1
    s = True
    while s:
        # if len(data) == 0:

            
            # print(data)
        for i in data:
            if 'password' in i:
                print('Смена пароля   ')

            elif 'personal' in i:
                adduser.User(\
                    i['personal']['firstName'],\
                    i['personal']['lastName'],\
                    i['personal']['middleName'],\
                    i['id'],\
                    i['roles'])
                
                # print(f"Создание изменение учетной записи   \n\
                #     {i['personal']['firstName']}\n,\
                #     {i['personal']['lastName']}\n,\
                #     {i['personal']['middleName']}\n,\
                #     {i['id']}\n,\
                #     {''.join(i['roles'])}\n")
                

            elif 'uuid' in i and len(i) == 1:
                print('блокировка учетки   ')

            elif 'name' in i and 'uuid' in i: 
                print('Создание изменение структуры   ')

            else:
                print('что-то')
        # k += 1
        data = []
        if len(data) == 0:
            s = False