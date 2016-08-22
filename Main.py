import requests
import xmltodict
import json
import sys


def smssend ():
    login=input('Введите логин= ')
    psw=input('Введите пароль= ')
    phones=input('Введите телефон 7...= ')
    mes=input('Введите сообщение= ')
    r = requests.get('http://smsc.ru/sys/send.php?login='+login+'&psw='+psw+'&phones='+phones+'&mes='+mes)
    print(r.text)
def multifon_routing():
    psw=input('Введите пароль= ')
    phones=input('Введите телефон 7...= ')
    r = requests.get('https://sm.megafon.ru/sm/client/routing?login='+phones+'@multifon.ru&password='+psw)
    #json_r = json.dumps(xmltodict.parse(r.text))
    json_r = xmltodict.parse(r.text)
    try:
        print('Результат = '+json_r['response']['routing'])
    except KeyError:
        print('Результат = ' + json_r['response']['result']['description'])


print('0 – только телефон')
print('1 – только в «МультиФон»')
print('2 – телефон и «МультиФон»')
routing=input('Выберите роутинг ')
phones=input('Введите телефон 7...= ')
psw=input('Введите пароль= ')
r = requests.get('https://sm.megafon.ru/sm/client/routing/set?login='+phones+'@multifon.ru&password='+psw+'&routing='+routing)
json_r = xmltodict.parse(r.text)
print(json_r)
print('Результат = ' + json_r['response']['result']['description'])