import csv
import imghdr
from time import sleep

from django.shortcuts import redirect, render
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib3.filepost import writer


def data_from_parser(data):
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
            stop += 1
            if stop == 2:
                break
            try:
                button = driver.find_elements(By.CLASS_NAME, 'btn')
                button[1].send_keys(Keys.ENTER)
                # sleep(5)
                type_name = driver.find_element(By.ID, 'filter_mi_mititle')
                type_name.send_keys(row['name'][0:5])  # Датчик давления
                type_sn = driver.find_element(By.ID, 'filter_mi_number')
                type_sn.send_keys(row['serial_number'])
                button = driver.find_element(By.CLASS_NAME, 'btn-primary')
                button.send_keys(Keys.ENTER)
                sleep(5)
                table_div = driver.find_element(By.CLASS_NAME, 'sticky-spinner-wrap')
                table_body = table_div.find_elements(By.TAG_NAME, 'tbody')
                # table_tr = table_body.find_elements(By.TAG_NAME, 'tr')
                # type_td = type_tr.find_elements(By.TAG_NAME, 'td')
                print('type_td')

            #     ООО "ГАЗИЗМЕРЕНИЯ"
            # 2022-10-31

            except:
                print('text')
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
