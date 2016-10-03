# coding: utf8
from tkinter import *
from tkinter import ttk
import APITM
import json
import urllib
import time
def delete_all():
    if (get_addresses_like_get_streets_var.get() != 'false')or ('false'!= get_addresses_like_get_points_var.get()):
        get_addresses_like_get_houses_var.set('false')
        get_addresses_like_house_var.set('')
        get_addresses_like_get_houses.configure(state='disabled')
        get_addresses_like_house.configure(state='disabled')
    elif  get_addresses_like_get_houses_var.get() =='true':
        get_addresses_like_house.configure(state='active')
    else :
        get_addresses_like_get_houses.configure(state='active')

strings2 = time.strftime("%Y,%m,%d,%H,%M,%S")
t2 = strings2.split(',')
def time_picker(rrrr):
    def change_month():

        if len(spinval_month.get()) == 1:
            spinval_month.set('0' + spinval_month.get())
    def change_day():
        if len(spinval_day.get()) == 1:
            spinval_day.set('0' + spinval_day.get())
    def change_hour():
        if len(spinval_hour.get()) == 1:
            spinval_hour.set('0' + spinval_hour.get())
    def change_minute():
        if len(spinval_minute.get()) == 1:
            spinval_minute.set('0' + spinval_minute.get())

    time_picker = Tk()
    strings = time.strftime("%Y,%m,%d,%H,%M,%S")
    t = strings.split(',')

    spinval_god = StringVar(time_picker)
    spinval_god.set(t[0])
    god = Spinbox(time_picker, from_=2014.0, to=2100.0, textvariable=spinval_god)
    god.pack()
    spinval_month = StringVar(time_picker)
    month = Spinbox(time_picker, from_=1.0, to=12.0, textvariable=spinval_month,command=change_month)
    spinval_month.set(t[1])
    month.pack()
    spinval_day = StringVar(time_picker)
    day = Spinbox(time_picker, from_=1.0, textvariable=spinval_day, to=31.0, command=change_day)
    spinval_day.set(t[2])
    day.pack()
    spinval_hour = StringVar(time_picker)
    hour = Spinbox(time_picker, from_=1.0, textvariable=spinval_hour, to=24.0, command=change_hour)
    spinval_hour.set(t[3])
    hour.pack()
    spinval_minute = StringVar(time_picker)
    minute = Spinbox(time_picker, from_=1.0, textvariable=spinval_minute, to=60.0, command=change_minute)
    spinval_minute.set(t[4])
    minute.pack()
    ttk.Button(time_picker, text="OK",command= lambda :calc_order_cost_time_var.set(god.get()+
                                                                                    month.get()+
                                                                                   day.get()+
                                                                                  hour.get()+
                                                                                 minute.get()+t[5])).pack()

    options.focus_force()

def request_API():

    if request.get() =='get_crew_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'crew_id':str(get_crew_info_crew_id.get())}, key=key.get()))
    elif request.get() =='get_driver_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'driver_id': str(driver_id.get())}, key=key.get()))
    elif request.get() =='get_crews_coords':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'crew_id': str(get_crews_coords_crew_id.get())}, key=key.get()))
    elif request.get() =='get_car_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'car_id': str(get_car_info_car_id.get())}, key=key.get()))
    elif request.get() =='get_drivers_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'locked_drivers': str(locked_drivers.get()),
                                                                                  'dismissed_drivers': str(locked_drivers.get())}, key=key.get()))
    elif request.get() =='get_cars_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'locked_cars': str(locked_cars.get()),
                                                                                  }, key=key.get()))
    elif request.get() =='get_crews_info':
        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param={'not_working_crews': str(not_working_crews.get())}, key=key.get()))
    elif request.get() =='calc_order_cost':

        param={'tariff_id': str(calc_order_cost_tariff_id.get()),
                   'source_time': str(calc_order_cost_time.get()),
               'is_prior': str(calc_order_cost_is_prior_var.get()),
                   'client_id': str(calc_order_cost_client_id.get()),
               'discount_id': str(calc_order_cost_discount_id.get()),
                   'disc_card_id': str(calc_order_cost_disc_card_id.get()),
               'source_zone_id': str(calc_order_cost_source_zone_id.get()),
                   'dest_zone_id': str(calc_order_cost_dest_zone_id.get()),
               'distance_city': str(calc_order_cost_distance_city.get()),
                   'distance_country': str(calc_order_cost_distance_country.get()),
               'source_distance_country': str(calc_order_cost_source_distance_country.get()),
                   'is_country': str(calc_order_cost_is_country_var.get()),
               'waiting_minutes': str(calc_order_cost_waiting_minutes.get()),
                   'is_hourly': str(calc_order_cost_is_hourly_var.get()),
               'hourly_minutes': str(calc_order_cost_hourly_minutes.get()),
                   'is_prize': str(calc_order_cost_is_prize_var.get()),
               'back_way': str(calc_order_cost_back_way_var.get()),
                   'services': str(calc_order_cost_services.get()),
               'order_params': str(calc_order_cost_order_params.get()),
                   'cashless': str(calc_order_cost_cashless_var.get())}
        param_cleare={}
        for _items in param:
            if param[_items]!='':
                param_cleare[_items]=param[_items]

        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param_cleare, key=key.get()))
    elif request.get() == 'change_order_state':
        answer = (APITM.POSTparamAPI(host.get(), port.get(), request.get(),
                                    param={'order_id': str(change_order_state_order_id.get()),'new_state': str(change_order_state_new_state.get())}, key=key.get()))
    elif request.get() =='get_addresses_like':

        param={
            'get_streets': str(get_addresses_like_get_streets_var.get()),
            'get_points' :str(get_addresses_like_get_points_var.get()),
            'get_houses':str(get_addresses_like_get_houses_var.get()),
            'search_in_tm': str(get_addresses_like_search_in_tm_var.get()),
            'search_in_yandex': str(get_addresses_like_search_in_yandex_var.get()),
            'search_in_google' :str(get_addresses_like_search_in_google_var.get()),
            'search_in_2gis' :str(get_addresses_like_search_in_2gis_var.get()),
            'city' :str(get_addresses_like_city.get()),
            'street': str(get_addresses_like_street.get()),
            'house' :str(get_addresses_like_house.get()),
            'max_addresses_count':str(get_addresses_like_max_addresses_count.get())
            }
        param_cleare={}
        for _items in param:
            if param[_items]!='':
                param_cleare[_items]=param[_items]

        answer = (APITM.GETparamAPI(host.get(), port.get(), request.get(), param_cleare, key=key.get()))
    else:
        answer=(APITM.GETparamAPI(host.get(),port.get(),request.get(),'',key.get()))
    request_listbox.delete('1.0', 'end')
    request_listbox.insert(END, json.dumps(answer[0], indent=4, sort_keys=True,ensure_ascii=False))
    answer_listbox.delete('1.0', 'end')
    answer_listbox.insert(END, answer[1])
def options_frame_print(rrrr):

    if request.get()=='get_crew_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        get_crew_info_crew_id.grid(row=2, column=1, sticky='W,E')
        get_crew_info_crew_id_L.grid(row=2, column=0, sticky='W,E')
    elif request.get()=='get_driver_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        driver_id.grid(row=2, column=1, sticky='W,E')
        driver_id_L.grid(row=2, column=0, sticky='W,E')
    elif request.get()=='get_crews_coords':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        get_crews_coords_crew_id.grid(row=2, column=1, sticky='W,E')
        get_crews_coords_crew_id_L.grid(row=2, column=0, sticky='W,E')

    elif request.get()=='get_car_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        get_car_info_car_id.grid(row=2, column=1, sticky='W,E')
        get_car_info_car_id_L.grid(row=2, column=0, sticky='W,E')

    elif request.get()=='get_drivers_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        locked_drivers_check.grid(row=2, column=1, sticky='W,E')
        dismissed_drivers_check.grid(row=2, column=0, sticky='W,E')
    elif request.get()=='get_cars_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        locked_cars_check.grid(row=2, column=1, sticky='W,E')
    elif request.get()=='get_crews_info':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        get_crews_info_check.grid(row=2, column=1, sticky='W,E')
    elif request.get()=='calc_order_cost':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        calc_order_cost_tariff_id_L.grid(row=0, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_tariff_id.grid(row=1, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_time_L.grid(row=0, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_time.grid(row=1, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_waiting_minutes_L.grid(row=0, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_waiting_minutes.grid(row=1, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_cashless_L.grid(row=0, column=3, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_cashless.grid(row=1, column=3, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_client_id_L.grid(row=2, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_client_id.grid(row=3, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_discount_id_L.grid(row=2, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_discount_id.grid(row=3, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_disc_card_id_L.grid(row=2, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_disc_card_id.grid(row=3, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_source_zone_id_L.grid(row=4, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_source_zone_id.grid(row=5, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_dest_zone_id_L.grid(row=4, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_dest_zone_id.grid(row=5, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_distance_city_L.grid(row=6, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_distance_city.grid(row=7, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_distance_country_L.grid(row=6, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_distance_country.grid(row=7, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_source_distance_country_L.grid(row=6, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_source_distance_country.grid(row=7, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_hourly_minutes_L.grid(row=8, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_hourly_minutes.grid(row=9, column=2, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_order_params_L.grid(row=8, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_order_params.grid(row=9, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_services_L.grid(row=8, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_services.grid(row=9, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_is_hourly.grid(row=10, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_is_prize.grid(row=10, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_back_way.grid(row=11, column=0, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_is_country.grid(row=11, column=1, columnspan=1, sticky='W,E,n,e')
        calc_order_cost_is_prior.grid(row=10, column=2, columnspan=1, sticky='W,E,n,e')

    elif request.get()=='change_order_state':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        change_order_state_order_id_L.grid(row=0, column=0, columnspan=1, sticky='W,E,n,e')
        change_order_state_order_id.grid(row=1, column=0, columnspan=1, sticky='W,E,n,e')
        change_order_state_new_state_L.grid(row=0, column=1, columnspan=1, sticky='W,E,n,e')
        change_order_state_new_state.grid(row=1, column=1, columnspan=1, sticky='W,E,n,e')

    elif request.get()=='get_addresses_like':
        for widget in options.winfo_children():
            widget.grid_forget()
        options.grid(row=2, column=0, columnspan=3, sticky='W,E,n,e')
        get_addresses_like_search_in_tm.grid(row=0, column=0, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_search_in_yandex.grid(row=0, column=1, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_search_in_google.grid(row=0, column=2, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_search_in_2gis.grid(row=0, column=3, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_get_streets.grid(row=1, column=0, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_get_points.grid(row=1, column=1, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_get_houses.grid(row=1, column=2, columnspan=1, sticky='W,E,n,e')

        get_addresses_like_city_L.grid(row=2, column=0, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_street_L.grid(row=2, column=1, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_house_L.grid(row=2, column=2, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_max_addresses_count_L.grid(row=2, column=3, columnspan=1, sticky='W,E,n,e')

        get_addresses_like_city.grid(row=3, column=0, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_street.grid(row=3, column=1, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_house.grid(row=3, column=2, columnspan=1, sticky='W,E,n,e')
        get_addresses_like_max_addresses_count.grid(row=3, column=3, columnspan=1, sticky='W,E,n,e')



    elif request.get()!='':
        options.grid_forget()

master = Tk()
master.grid_columnconfigure(0, weight=1)
#master.grid_rowconfigure(0, weight=1)
#Описание контролов
requestvar = StringVar(master)
API_request = ('ping',
               'get_crew_groups_list',
               'get_client_groups_list',
               'get_tariffs_list',
               'get_services_list',
               'get_order_params_list',
               'get_discounts_list',
               'calc_order_cost',
               'get_crew_info',
               'change_order_state',
               'get_crews_info',
               'get_driver_info',
               'get_drivers_info',
               'get_uds_list',
               'get_order_params_list',
               'get_car_info',
               'get_cars_info',
               'get_crews_coords',
               'get_addresses_like')
request = ttk.Combobox(master, textvariable=requestvar, values=API_request,state='readonly')#,postcommand=options_frame_print)
request.bind("<FocusIn>", options_frame_print)
#request.current(0)
button = ttk.Button(master, text="OK",command=request_API)
host_L=ttk.Label(master, text='Хост')
port_L=ttk.Label(master, text='Порт')
key_L=ttk.Label(master, text='Секретный ключ')
request_frame = ttk.Frame(master,height=300, width=300)
options = ttk.Frame(master)
request_listbox= Text(request_frame,height=30, width=30)
answer_frame = ttk.Frame(master)
answer_listbox= Text(answer_frame,height=30, width=30)
host=ttk.Entry(master)
host.insert(0, "127.0.0.1")
port=ttk.Entry(master)
port.insert(0, "8090")
key=ttk.Entry(master)
key.insert(0, "12345")
get_crew_info_crew_id_L=ttk.Label(options, text='Ид экипажа')
get_crew_info_crew_id= ttk.Entry(options)

get_crews_coords_crew_id_L=ttk.Label(options, text='Ид экипажа')
get_crews_coords_crew_id= ttk.Entry(options)

driver_id_L=ttk.Label(options, text='Ид водителя')
driver_id= ttk.Entry(options)

get_crews_info_crew_id_L=ttk.Label(options, text='ИД экипажа, по которому нужно вернуть координаты.\nЕсли не задано, то будут возвращены координаты всех экипажей на линии.')
get_crews_info_crew_id= ttk.Entry(options)

get_car_info_car_id_L=ttk.Label(options, text='Ид автомобиля')
get_car_info_car_id= ttk.Entry(options)


locked_drivers = StringVar()
locked_drivers.set('false')
locked_drivers_check = ttk.Checkbutton(options,
                                       text='Включить в ответ запроса заблокированных водителей (по умолчанию false)',
                                       variable=locked_drivers,
                                       onvalue='true',
                                       offvalue='false')

dismissed_drivers = StringVar()
dismissed_drivers.set('false')
dismissed_drivers_check = ttk.Checkbutton(options,
                                          text='Включить в ответ запроса уволенных водителей (по умолчанию false)',
                                          variable=dismissed_drivers,
                                          onvalue='true',
                                          offvalue='false'
                                          )
not_working_crews = StringVar()
not_working_crews.set('false')
get_crews_info_check = ttk.Checkbutton(options,
                                          text='Включить в ответ экипажи не на линии',
                                          variable=not_working_crews,
                                          onvalue='true',
                                          offvalue='false'
                                          )

#calc_order_cost интерфейс
calc_order_cost_tariff_id_L=ttk.Label(options, text='Ид тарифа')
calc_order_cost_tariff_id= ttk.Entry(options)
calc_order_cost_time_var = StringVar(options)
calc_order_cost_time_var.set(t2[0] + t2[1] + t2[2] + t2[3] + t2[4] + t2[5])
calc_order_cost_time_L= ttk.Label(options, text='Время')
calc_order_cost_time=ttk.Entry(options,textvariable=calc_order_cost_time_var)
calc_order_cost_time.bind("<FocusIn>", time_picker)
calc_order_cost_waiting_minutes_L=ttk.Label(options, text='Ожидание мин')
calc_order_cost_waiting_minutes= ttk.Entry(options)
calc_order_cost_cashless_L=ttk.Label(options, text='Безнал')
calc_order_cost_cashless_var = StringVar(options)
calc_order_cost_cashless = ttk.Checkbutton(options,
                                          text='Безналичный расчет',
                                          variable=calc_order_cost_cashless_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_cashless_var.set('false')
calc_order_cost_client_id_L=ttk.Label(options, text='Ид клиента')
calc_order_cost_client_id= ttk.Entry(options)
calc_order_cost_discount_id_L=ttk.Label(options, text='Ид скидки')
calc_order_cost_discount_id= ttk.Entry(options)
calc_order_cost_disc_card_id_L=ttk.Label(options, text='Ид дисконтной карты')
calc_order_cost_disc_card_id=ttk.Entry(options)
calc_order_cost_source_zone_id_L=ttk.Label(options, text='Ид района подачи')
calc_order_cost_source_zone_id=ttk.Entry(options)
calc_order_cost_dest_zone_id_L=ttk.Label(options, text='Ид района назначения')
calc_order_cost_dest_zone_id=ttk.Entry(options)
calc_order_cost_distance_city_L=ttk.Label(options, text='Городской километраж')
calc_order_cost_distance_city=ttk.Entry(options)
calc_order_cost_distance_country_L=ttk.Label(options, text='Загородный километраж')
calc_order_cost_distance_country=ttk.Entry(options)
calc_order_cost_source_distance_country_L=ttk.Label(options, text='Километраж до подачи загородом')
calc_order_cost_source_distance_country=ttk.Entry(options)
calc_order_cost_hourly_minutes_L=ttk.Label(options, text='Длительность почасового')
calc_order_cost_hourly_minutes=ttk.Entry(options)
calc_order_cost_services_L=ttk.Label(options, text='Услуги через ;')
calc_order_cost_services=ttk.Entry(options)
calc_order_cost_order_params_L=ttk.Label(options, text='Параметры через ;')
calc_order_cost_order_params=ttk.Entry(options)
calc_order_cost_is_hourly_var = StringVar(options)
calc_order_cost_is_hourly = ttk.Checkbutton(options,
                                          text='Почасовой',
                                          variable=calc_order_cost_is_hourly_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_is_hourly_var.set('false')
calc_order_cost_is_prize_var = StringVar(options)
calc_order_cost_is_prize = ttk.Checkbutton(options,
                                          text='Призовой',
                                          variable=calc_order_cost_is_prize_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_is_prize_var.set('false')
calc_order_cost_back_way_var = StringVar(options)
calc_order_cost_back_way = ttk.Checkbutton(options,
                                          text='Обратный путь',
                                          variable=calc_order_cost_back_way_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_back_way_var.set('false')
calc_order_cost_is_country_var = StringVar(options)
calc_order_cost_is_country = ttk.Checkbutton(options,
                                          text='Загородный',
                                          variable=calc_order_cost_is_country_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_is_country_var.set('false')
calc_order_cost_is_prior_var = StringVar(options)
calc_order_cost_is_prior = ttk.Checkbutton(options,
                                          text='Предварительный',
                                          variable=calc_order_cost_is_country_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
calc_order_cost_is_prior_var.set('false')
# /common_api/1.0/change_order_state

change_order_state_order_id_L=ttk.Label(options, text='ИД заказа')
change_order_state_order_id=ttk.Entry(options)
change_order_state_new_state_L=ttk.Label(options, text='Новый статус')
change_order_state_new_state=ttk.Entry(options)

locked_cars = StringVar()
locked_cars.set('false')
locked_cars_check = ttk.Checkbutton(options,
                                       text='Включить в ответ заблокированных автомобилей (по умолчанию false)',
                                       variable=locked_cars,
                                       onvalue='true',
                                       offvalue='false')
#GET /common_api/1.0/get_addresses_like?
get_addresses_like_get_streets_var = StringVar(options)
get_addresses_like_get_streets = ttk.Checkbutton(options,
                                          text='Искать улицы',
                                          variable=get_addresses_like_get_streets_var,
                                          onvalue='true',
                                          offvalue='false',
                                            command = delete_all

                                          )
get_addresses_like_get_streets_var.set('false')



get_addresses_like_get_points_var = StringVar(options)
get_addresses_like_get_points = ttk.Checkbutton(options,
                                          text='Искать пункты',
                                          variable=get_addresses_like_get_points_var,
                                          onvalue='true',
                                          offvalue='false',
                                                command = delete_all
                                          )
get_addresses_like_get_points_var.set('false')

get_addresses_like_get_houses_var = StringVar(options)
get_addresses_like_get_houses = ttk.Checkbutton(options,
                                          text='Искать дома',
                                          variable=get_addresses_like_get_houses_var,
                                          onvalue='true',
                                          offvalue='false',
                                            command = delete_all
                                          )
get_addresses_like_get_houses_var.set('false')



get_addresses_like_search_in_tm_var = StringVar(options)
get_addresses_like_search_in_tm = ttk.Checkbutton(options,
                                          text='Искать в ТМ',
                                          variable=get_addresses_like_search_in_tm_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
get_addresses_like_search_in_tm_var.set('false')

get_addresses_like_search_in_yandex_var = StringVar(options)
get_addresses_like_search_in_yandex = ttk.Checkbutton(options,
                                          text='Искать в яндексе',
                                          variable=get_addresses_like_search_in_yandex_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
get_addresses_like_search_in_yandex_var.set('false')

get_addresses_like_search_in_google_var = StringVar(options)
get_addresses_like_search_in_google = ttk.Checkbutton(options,
                                          text='Искать в гугле',
                                          variable=get_addresses_like_search_in_google_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
get_addresses_like_search_in_google_var.set('false')

get_addresses_like_search_in_2gis_var = StringVar(options)
get_addresses_like_search_in_2gis = ttk.Checkbutton(options,
                                          text='Искать в 2ГИС',
                                          variable=get_addresses_like_search_in_2gis_var,
                                          onvalue='true',
                                          offvalue='false'
                                          )
get_addresses_like_search_in_2gis_var.set('false')

get_addresses_like_city_L=ttk.Label(options, text='Город')
get_addresses_like_city=ttk.Entry(options)

get_addresses_like_street_L=ttk.Label(options, text='Часть названия улицы или пункта')
get_addresses_like_street=ttk.Entry(options)
get_addresses_like_house_var = StringVar(options)
get_addresses_like_house_var.set('')
get_addresses_like_house_L=ttk.Label(options, text='Часть номера дома',textvariable=get_addresses_like_house_var)
get_addresses_like_house=ttk.Entry(options)
get_addresses_like_max_addresses_count_L=ttk.Label(options, text='Максимальное число адресов в ответе')
get_addresses_like_max_addresses_count=ttk.Entry(options)

#Сборка ебучих кнопок
host_L.grid(row=0, column=0, sticky='W,E')
port_L.grid(row=0, column=1, sticky='W,E')
key_L.grid(row=0, column=2, sticky='W,E')
host.grid(row=1, column=0, sticky='W,E')
port.grid(row=1, column=1, sticky='W,E')
key.grid(row=1, column=2, sticky='W,E')
button.grid(row=3, column=1, columnspan=2,sticky='W,E')
request.grid(row=3, column=0, sticky='W,E')
request_frame.grid(row=4, column=0, sticky='W,E,n,e')
answer_frame.grid(row=4, column=1, columnspan=2, sticky='W,E,n,e')
answer_listbox.pack(fill='both')
request_listbox.pack(fill='both')



mainloop()