import requests
import xmltodict

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
    print('Результат = ' + json_r['response']['result']['description'])

while 1:
    print('Что делать будем ?')
    print('Отправим смску через смсц(1)')
    print('Узнаем роутинг мультифона(2)')
    print('Выставим роутинг мультифона?(3)')
    print('ВЫХОД(EXIT)(ЕХИТ)(ЗАКРЫТЬ)(4)')
    choice = input('Выбор =: ')
    if choice == '1':
        smssend()
    elif choice == '2':
        multifon_routing()
    elif choice=='3':
        multifon_set_routing()
    elif choice=='4':
        break
    else:
        print('ЭЭЭЭЭЭЭЭ че ты ввел то ? Давайка заного!')
