# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:51:28 2020

@author: yasin
"""

#import packages
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome('./chromedriver')
wait = WebDriverWait(driver,10)


#get raw data
def get_dt_field(driver):
    return driver.find_element_by_css_selector('#tarih')

domain = 'https://www.turkiye.gov.tr' 
cities = ['istanbul']

for year in [2017,2018,2019,2020]:
    dfs = []
    for city in cities:
        url = f'{domain}/{city}-buyuksehir-belediyesi-vefat-sorgulama'
        for dt in pd.date_range(f'{year}-02-01',f'{year}-04-12'):
            driver.get(url)
            e = wait.until(get_dt_field) 
            e.clear()
            e.send_keys(f'{dt.strftime("%d/%m/%Y")}\n')
            source = driver.page_source
            try:
                df = pd.read_html(source)[0]
                df['day'] = dt
                df['city'] = city
                dfs.append(df)
            except:
                print(f'No deaths on {day} in {city}')
    df = pd.concat(dfs).drop('İşlem',axis=1)
    df.to_csv(f'{year}_raw.csv',index=False)
    
# clean the data
from glob import glob
dfs = [pd.read_csv(f,na_values=['-']) for f in glob('*raw*.csv')]
df = pd.concat(dfs).reset_index(drop=True)
df['day'] = pd.to_datetime(df['day'])

df = df.rename(columns={'day':'Ölüm Tarihi'})

#Save the data as csv file
df.to_csv('istanbul_deathtoll_data.csv',index=False)

