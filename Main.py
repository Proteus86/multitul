import requests
import xmltodict
import json
import csv
import APITM
from fdb import services


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
    json_r = xmltodict.parse(r.text)
    try:
        print('Результат = '+json_r['response']['routing']+'\n')
    except KeyError:
        print('Результат = ' + json_r['response']['result']['description']+'\n')

def multifon_set_routing():
    print('0 – только телефон')
    print('1 – только в «МультиФон»')
    print('2 – телефон и «МультиФон»')
    routing=input('Выберите роутинг ')
    phones=input('Введите телефон 7...= ')
    psw=input('Введите пароль= ')
    r = requests.get('https://sm.megafon.ru/sm/client/routing/set?login='+phones+'@multifon.ru&password='+psw+'&routing='+routing)
    json_r = xmltodict.parse(r.text)
    print(json_r)
    print('Результат = ' + json_r['response']['result']['description']+'\n')

def poisk_region():
    town=input('Введите город ')
    key=input('Введите ключ ')
    r = requests.get('http://catalog.api.2gis.ru/geo/search?q=' + town + '&types=city,settlement&format=short&version=1.3&key=' + key)
    decoded = json.loads(r.text)
    try:
        list = decoded['result']
        print('Регион= '+str(list[0]['project_id'])+'\n')
    except:
        print('error_message= ' + decoded['error_message']+'\n')
        print('error_code= ' + decoded['error_code']+'\n')

def poisk_region_coords():
    town = input('Введите город ')
    key = input('Введите ключ ')
    r = requests.get(
        'http://catalog.api.2gis.ru/geo/search?q=' + town + '&types=city,settlement&output=xml&version=1.3&key=' + key)
    json_r = xmltodict.parse(r.text)
    try:
        string = str(json_r['root']['result']['geoObject']['selection'])
        MULTI = (string.find('MULTI'))
        if MULTI == 0:
            string = string.lstrip('MULTIPOLYGON(((')
            number = (string.find('))'))
            string = string[:number]
            q = string.split(' ')
            q_last = q.pop()
            q_first = q.pop(0)
            q_all = q_first + ',' + q_last
            q.append(q_all)
            with open(town+'.csv', 'w', newline="") as f:
                writer = csv.writer(f)
                for i in q:
                    string = i.split(',')
                    writer.writerow(string)
        else:
            string = string.lstrip('POLYGON((')
            string = string.rstrip('))')
            q = string.split(' ')
            q_last = q.pop()
            q_first = q.pop(0)
            q_all = q_first + ',' + q_last
            q.append(q_all)
            with open(town+'.csv', 'w', newline="") as f:
                writer = csv.writer(f)
                for i in q:
                    string = i.split(',')
                    writer.writerow(string)
    except:
        print('error_message= ' + json_r['root']['error_message'])
        print('error_code= ' + json_r['root']['error_code']+'\n')

def API_TM():
    print('GETparamAPI(ip, port, request, param='', key='') = 1')
    print('POSTparamAPI(ip, port, request, param='', key='', _json=False) = 2')
    print('GETparamTAPI(ip, port, request, param='', fields='', key='') = 3')
    print('POSTparamTAPI(ip, port, request, param='', key='') = 4\n')
    print('Выход = 5\n')
    choice = input('Ваш выбор =: ')
    if choice == '1':
        ip =input('ip= ')
        port =input('port= ')
        request =input('request= ')
        param =input('param= ')
        key =input('key= ')
        print(APITM.GETparamAPI(ip, port, request, param, key))
    elif choice == '2':
        ip =input('ip= ')
        port =input('port= ')
        request =input('request= ')
        param =input('param= ')
        key =input('key= ')
        APITM.POSTparamAPI(ip, port, request, param, key)
    elif choice=='3':
        ip = input('ip= ')
        port = input('port= ')
        request = input('request= ')
        param = input('param= ')
        fields = input('fields= ')
        key = input('key= ')
        APITM.GETparamTAPI(ip, port, request, param, fields, key)
    elif choice=='4':
        ip = input('ip= ')
        port = input('port= ')
        request = input('request= ')
        param = input('param= ')
        key = input('key= ')
        APITM.POSTparamTAPI(ip, port, request, param, key)
    elif choice=='5':
        return
    else:
        print('ЭЭЭЭЭЭЭЭ че ты ввел то ? Давайка заного !\n')

def services_API_backup():
    base = input('Путь к локальной базе ')
    base_backup = input('Путь к бэкапу ')
    host = input("host= 127.0.0.1 ")
    user = input("user = sysdba ")
    password = input("password = admin ")
    con = services.connect(host=host, user=user, password=password)
    con.backup(base, base_backup, collect_garbage=True)
    backup_report = con.readlines()
    f = open('backup_report.txt', 'w')
    print('Лог лежит в файле backup_report.txt')
    f.write(base + " " + base_backup + "\n" + "\n")
    for i in backup_report:
        f.write(i + '\n')
        print(i)
    f.close()


def oktell():
    while 1:
        number = input('Номер/q выход(все другое сброс звонка) ')
        if number.isdigit():
            requests.get('http://127.0.0.1:4059/callto?number=' + number)
        elif number == 'q':
            break
        else:
            requests.get('http://127.0.0.1:4059/disconnectcall')

while 1:
    print('\n***********************************')
    print('Что делать будем ?')
    print('Отправим смску через смсц(1)')
    print('Узнаем роутинг мультифона(2)')
    print('Выставим роутинг мультифона?(3)')
    print('Поиском региона 2ГИС по городу?(4)')
    print('Выгрузим координаты города по названию ?(5)')
    print('Запрос в АПИ ТМ ?(6)')
    print('Бэкап базы *.FDB ?(7)')
    print('Oktell ?(8)')
    print('ВЫХОД(EXIT)(ЕХИТ)(ЗАКРЫТЬ)(q)')
    print('***********************************\n')
    choice = input('Выбор =: ')
    if choice == '1':
        smssend()
    elif choice =='2':
        multifon_routing()
    elif choice=='3':
        multifon_set_routing()
    elif choice=='4':
        poisk_region()
    elif choice=='5':
        poisk_region_coords()
    elif choice=='6':
        API_TM()
    elif choice=='7':
        services_API_backup()
    elif choice=='8':
        oktell()
    elif choice=='q':
        break
    else:
        print('ЭЭЭЭЭЭЭЭ че ты ввел то ? Давайка заного !\n')
