from tkinter import *
from tkinter import ttk
import requests
import xmltodict
import json
import csv
import APITM
from fdb import services
import fdb
import time
import threading
from tkinter import messagebox


def Quit():
    global root
    root.destroy()
    root.quit()
def sms_Quit():
    global sms_root
    sms_root.destroy()
    sms_root.quit()
def multifon_main_quit():
    global multifon_main
    multifon_main.destroy()
    multifon_main.quit()
def poisk_region_quit():
    global poisk_region_main
    poisk_region_main.destroy()
    poisk_region_main.quit()
def poisk_region_coords_quit():
    global poisk_region_coords
    poisk_region_coords.destroy()
    poisk_region_coords.quit()

def sms():
    def make_menu(w):
        global the_menu
        the_menu = Menu(w, tearoff=0)
        the_menu.add_command(label="Cut")
        the_menu.add_command(label="Copy")
        the_menu.add_command(label="Paste")
    def show_menu(e):
        w = e.widget
        the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
        the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
        the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
        the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
    def paste_clipboard(event):
        event.widget.delete(0, 'end')
        event.widget.insert(0, sms_root.clipboard_get())

    def smssend():
        global dict_entry
        r = requests.get('http://smsc.ru/sys/send.php?'
                         'login=' + dict_entry['login'].get() +
                         '&psw=' + dict_entry['passw'].get() +
                         '&phones=' + dict_entry['phone'].get() +
                         '&mes=' + dict_entry['msg'].get())
        label.config(text=r.text)
    global sms_root
    sms_root = Tk()
    make_menu(sms_root)
    sms_root.title("Отправка СМС")
    sms_root.protocol('WM_DELETE_WINDOW', sms_Quit)
    global dict_entry
    dict_entry={}
    for s in ["login", "passw", "phone","msg"]:
        key =s
        s = ttk.Entry(sms_root);s.pack()
        s1 = ttk.Label(sms_root,text=key);s1.pack()
        s.bind('<ButtonRelease-2>', paste_clipboard)
        s.bind('<ButtonRelease-3>', show_menu)
        dict_entry [key]=s
    label = ttk.Label(sms_root);label.pack()
    ttk.Button(sms_root, text="Отправить", command=smssend).pack()
    ttk.Button(sms_root,text="ВЫХОД(EXIT)", command=sms_Quit).pack()
    sms_root.focus_set()
    sms_root.mainloop()
def multifon():
    global dict_entry
    global multifon_main
    global var1
    def multifon_routing():
        global dict_entry
        r = requests.get('https://sm.megafon.ru/sm/client/routing?login=' +  dict_entry['number'].get() + '@multifon.ru&password=' + dict_entry['passw'].get())
        json_r = xmltodict.parse(r.text)
        try:
            if json_r['response']['routing'] == '1':
                label_chek.config(text='только в «МультиФон»')
            elif json_r['response']['routing'] == '0':
                label_chek.config(text='только  телефон')
            elif json_r['response']['routing'] == '2':
                label_chek.config(text='телефон и «МультиФон»')
        except KeyError:
            label_chek.config(text=json_r['response']['result']['description'])
    def multifon_set_routing():
        global dict_entry
        r = requests.get('https://sm.megafon.ru/sm/client/routing/set?login='
                         + dict_entry['number'].get()
                         + '@multifon.ru&password='
                         + dict_entry['passw'].get()
                         + '&routing=' + str(var1.get()))
        json_r = xmltodict.parse(r.text)
        label_set.config(text='Результат = ' + json_r['response']['result']['description'])
    def make_menu(w):
        global the_menu
        the_menu = Menu(w, tearoff=0)
        the_menu.add_command(label="Cut")
        the_menu.add_command(label="Copy")
        the_menu.add_command(label="Paste")
    def show_menu(e):
        w = e.widget
        the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
        the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
        the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
        the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
    def paste_clipboard(event):
        event.widget.delete(0, 'end')
        event.widget.insert(0, multifon_main.clipboard_get())

    multifon_main=Tk()
    make_menu(multifon_main)
    dict_entry={}


    for s in ["number", "passw"]:
        key =s
        s = ttk.Entry(multifon_main,text=key);s.pack()
        s1 = ttk.Label(multifon_main, text=key); s1.pack()
        s.bind('<ButtonRelease-2>', paste_clipboard)
        s.bind('<ButtonRelease-3>', show_menu)
        dict_entry [key]=s
    ttk.Button(multifon_main, text="Проверить", command=multifon_routing).pack()
    label_chek = ttk.Label(multifon_main);label_chek.pack()
    ttk.Button(multifon_main, text="Переключить", command=multifon_set_routing).pack()
    var1 = IntVar(multifon_main)
    ttk.Radiobutton(multifon_main, text=r'только телефон', variable=var1, value=0).pack(anchor = W)
    ttk.Radiobutton(multifon_main, text=r'только в «МультиФон»', variable=var1, value=1).pack(anchor = W)
    ttk.Radiobutton(multifon_main, text=r'телефон и «МультиФон»', variable=var1, value=2).pack(anchor = W)
    label_set = ttk.Label(multifon_main);label_set.pack()
    ttk.Button(multifon_main, text="ВЫХОД(EXIT)", command=multifon_main_quit).pack()
    multifon_main.focus_set()
    multifon_main.mainloop()
def poisk_region():
    def show_menu(e):
        w = e.widget
        the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
        the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
        the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
        the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
    def make_menu(w):
        global the_menu
        the_menu = Menu(w, tearoff=0)
        the_menu.add_command(label="Cut")
        the_menu.add_command(label="Copy")
        the_menu.add_command(label="Paste")
    global dict_entry
    global poisk_region_main
    dict_entry={}
    poisk_region_main=Tk()
    make_menu(poisk_region_main)
    def paste_clipboard(event):
        event.widget.delete(0, 'end')
        event.widget.insert(0, poisk_region_main.clipboard_get())
    def poisk():
        global dict_entry
        r = requests.get('http://catalog.api.2gis.ru/geo/search?q='
                         + dict_entry['town'].get() +
                         '&types=city,settlement'
                        '&format=short&version=1.3'
                         '&key=' + dict_entry['key'].get())
        decoded = json.loads(r.text)
        try:
            list = decoded['result']
            label_region.config(text='Регион= '+str(list[0]['project_id']))
        except:

            label_region.config(text='error_message= ' + decoded['error_message']+' '+'\n error_code= ' + decoded['error_code'])

    for s in ["town", "key"]:
        key =s
        s = ttk.Entry(poisk_region_main,text=key);s.pack()
        s1 = ttk.Label(poisk_region_main, text=key); s1.pack()
        s.bind('<ButtonRelease-2>', paste_clipboard)
        s.bind('<ButtonRelease-3>', show_menu)
        dict_entry [key]=s
    label_region = ttk.Label(poisk_region_main, text='');label_region.pack()
    ttk.Button(poisk_region_main, text="Найти", command=poisk).pack()
    ttk.Button(poisk_region_main, text="ВЫХОД(EXIT)", command=poisk_region_quit).pack()

    poisk_region_main.focus_set()
    poisk_region_main.mainloop()

def poisk_region_coords():
    global poisk_region_coords
    global dict_entry
    def paste_clipboard(event):
        event.widget.delete(0, 'end')
        event.widget.insert(0, poisk_region_coords.clipboard_get())
    def show_menu(e):
        w = e.widget
        the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
        the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
        the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
        the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
    def make_menu(w):
        global the_menu
        the_menu = Menu(w, tearoff=0)
        the_menu.add_command(label="Cut")
        the_menu.add_command(label="Copy")
        the_menu.add_command(label="Paste")

    def poisk_coords():
        global dict_entry
        global poisk_region_coords
        town = dict_entry['town'].get()
        key = dict_entry['key'].get()
        r = requests.get(
            'http://catalog.api.2gis.ru/geo/search?q=' + town + '&types=city,settlement&output=xml&version=1.3&key=' + key)
        json_r = xmltodict.parse(r.text)
        try:
            string = str(json_r['root']['result']['geoObject']['selection'])
            s = string.find('),(')
            string = string.lstrip('MULTIPOLYGON(((')
            string = string.replace(')))', '')
            string = string.replace('POLYGON((', '')
            string = string.replace('))', '')
            if s == -1:
                q = string.split(' ')
                q_last = q.pop()
                q_first = q.pop(0)
                q_all = q_last + ',' + q_first
                q.append(q_all)
                with open(town + '.csv', 'w', newline="") as f:
                    writer = csv.writer(f)
                    for i in q:
                        string = i.split(',')
                        writer.writerow(string)
            else:
                string = string.split('),(')
                i = 0
                name = 1
                for i in string:
                    q = i.split(' ')
                    q_last = q.pop()
                    q_first = q.pop(0)
                    q_all = q_last + ',' + q_first
                    q.append(q_all)
                    with open(town + str(name) + '.csv', 'w', newline="") as f:
                        writer = csv.writer(f)
                        for i in q:
                            string = i.split(',')
                            writer.writerow(string)
                    name = name + 1
            messagebox.showinfo('Инфо', 'Все готово')
            poisk_region_coords.focus_set()
            poisk_region_coords.focus_force()
        except:
            messagebox.showwarning('Error', 'error_message= ' + json_r['root']['error_message']+'\n'+'error_code= ' + json_r['root']['error_code'] + '\n')
            poisk_region_coords.focus_set()
            poisk_region_coords.focus_force()

    dict_entry={}
    poisk_region_coords = Tk()
    make_menu(poisk_region_coords)
    for s in ["town", "key"]:
        key =s
        s = ttk.Entry(poisk_region_coords,text=key);s.pack()
        s1 = ttk.Label(poisk_region_coords, text=key); s1.pack()
        s.bind('<ButtonRelease-2>', paste_clipboard)
        s.bind('<ButtonRelease-3>', show_menu)
        dict_entry [key]=s
    ttk.Button(poisk_region_coords, text="Найти", command=poisk_coords).pack()
    ttk.Button(poisk_region_coords, text="ВЫХОД(EXIT)", command=poisk_region_coords_quit).pack()
    poisk_region_coords.focus_force()
    poisk_region_coords.mainloop()

root = Tk()
root.title("Главное")
'***************************************************'
sms = ttk.Button(text="Отправим смску через смсц", style="C.TButton", command=sms).pack()
multifon = ttk.Button(text="Узнаем роутинг мультифона", style="C.TButton", command=multifon).pack()
gis2 = ttk.Button(text="Поиском региона 2ГИС по городу", style="C.TButton", command=poisk_region).pack()
coords_town = ttk.Button(text="Выгрузим координаты города по названию", style="C.TButton", command=poisk_region_coords).pack()
'***************************************************'
API = ttk.Button(text="Запрос в АПИ ТМ", style="C.TButton").pack()
backup = ttk.Button(text="Бэкап базы *.FDB", style="C.TButton").pack()
oktell = ttk.Button(text="Oktell", style="C.TButton").pack()
tracert = ttk.Button(text="Запустить Tracert", style="C.TButton").pack()
exit = ttk.Button(text="ВЫХОД(EXIT)", style="C.TButton", command=Quit).pack()
root.protocol('WM_DELETE_WINDOW', Quit)
root.mainloop()