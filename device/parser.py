import csv
import re
from datetime import datetime
from time import sleep

from django.shortcuts import redirect
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def get_sample(table_tr):
    low_date = datetime.strptime('01-01-2000', '%d-%m-%Y').date()
    sample_data = ('error',)
    for i in table_tr:
        type_td = i.find_elements(By.TAG_NAME, 'td')
        try:
            if low_date < datetime.strptime('-'.join(type_td[6].text.split('.')), '%d-%m-%Y').date():
                low_date = datetime.strptime('-'.join(type_td[6].text.split('.')), '%d-%m-%Y').date()
                sample_data = ()
                for j in type_td:
                    sample_data += (j.text,)
        except:
            pass

    sleep(1)
    return sample_data


def data_from_parser(request):
    # "/home/andrei/chrome-linux64/"
    driver = webdriver.Chrome()
    driver.get("https://fgis.gost.ru/fundmetrology/cm/results?activeYear=%D0%92%D1%81%D0%B5")
    data_ = driver.find_element(By.CLASS_NAME, 'modal-footer')
    button = data_.find_element(By.TAG_NAME, 'button')
    button.send_keys(Keys.ENTER)
    stop = 0
    with open('./sample_send.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # stop += 1
            # if stop == 2:
            #     break
            try:
                button = driver.find_elements(By.CLASS_NAME, 'btn')
                button[1].send_keys(Keys.ENTER)
                sleep(3)
                type_model = driver.find_element(By.ID, 'filter_mi_modification')
                type_name = driver.find_element(By.ID, 'filter_mi_mititle')
                type_sn = driver.find_element(By.ID, 'filter_mi_number')
                my_string = ''.join(i for i in row['serial_number'] if not i.isalpha())
                type_sn.clear()
                type_sn.send_keys(my_string)
                type_name.clear()
                type_name.send_keys(row['name'][0:5])
                type_model.clear()
                type_model.send_keys(row['model'][0:2])
                sleep(5)
                btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')
                btn[0].send_keys(Keys.ENTER)
                sleep(5)
                table_div = driver.find_element(By.CLASS_NAME, 'sticky-spinner-wrap')
                table_tr = table_div.find_elements(By.TAG_NAME, 'tr')
            except:
                print('text')
            print(get_sample(table_tr, ))


    # <a href="/fundmetrology/registry" class="btn btn-lg btn-success btn-block ng-scope"><span class="fa fa-globe"></span> Публичный портал</a>
    # <div data-v-10e5d5a7="" class="col"><input data-v-10e5d5a7="" type="checkbox" id="hide-forever"> <label data-v-10e5d5a7="" for="hide-forever">Больше не показывать</label></div>
    # driver.close()
    #
    # with open('./sample_send.csv', encoding='utf-8') as f:
    #     reader = csv.DictReader(f, delimiter=';')
    # for row in reader:
    # print(row['serial_number'], row['type'], row['model'])

    # УКПГ-2 КГКМ ООО Газпром добыча Иркутск

    return redirect('/')
