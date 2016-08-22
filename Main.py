import requests

#r = requests.get('http://smsc.ru/sys/send.php?login=taximasterTP&psw=eirbvrvr&phones=79043165252&mes=привет%20как%20делы')
r = requests.get('http://nigma.ru/')
print (r.status_code)
print (r.headers['content-type'])
print(r.text)
