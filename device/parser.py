import csv
import re
from datetime import datetime
from time import sleep
from django.shortcuts import redirect
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from equipment.settings import BASE_DIR


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


def data_from_parser(data):
    "/home/andrei/chrome-linux64/"
    driver = webdriver.Chrome()
    driver.get("https://fgis.gost.ru/fundmetrology/cm/results?activeYear=%D0%92%D1%81%D0%B5")
    data_ = driver.find_element(By.CLASS_NAME, 'modal-footer')
    button = data_.find_element(By.TAG_NAME, 'button')
    button.send_keys(Keys.ENTER)
    stop = 0
    wb = load_workbook(f'{BASE_DIR}/from sending.xlsx')
    ws = wb['l1']
    for i, eq in enumerate(ws):
        stop += 1
        if stop == 2:
            break
        try:
            button = driver.find_elements(By.CLASS_NAME, 'btn')
            button[1].send_keys(Keys.ENTER)
            sleep(3)
            name = driver.find_element(By.ID, 'filter_mi_mititle')
            serial_number = driver.find_element(By.ID, 'filter_mi_number')
            org = driver.find_element(By.ID, 'filter_org_title')
            org.clear()
            sleep(2)
            org.send_keys('ИРКУТСКИЙ')
            sleep(2)
            serial_number.clear()
            sleep(2)
            serial_number.send_keys(ws[f'B{i + 2}'].value)
            sleep(2)
            name.clear()
            sleep(2)
            name.send_keys(ws[f'F{i + 2}'].value[0:4])
            sleep(5)
            btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')
            btn[0].send_keys(Keys.ENTER)
            sleep(5)
            table_div = driver.find_element(By.CLASS_NAME, 'sticky-spinner-wrap')
            table_tr = table_div.find_elements(By.TAG_NAME, 'tr')
            sleep(5)
            for row in table_tr:
                table_td = row.find_elements(By.TAG_NAME, 'td')
                print(table_td[2].text)

                # print('row text', row.text)

        except:
            print('error', ws[f'B{i + 2}'].value)

    return redirect('/')
