from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import re
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("disable-gpu")
driver=wd.Chrome(executable_path = 'C:/chromedriver.exe',options=options)


__all__=['google_store_app']

class google_store_app:
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("disable-gpu")
    driver=wd.Chrome(executable_path = 'C:/chromedriver.exe',options=options)
    
    def get_reviews(url):

        driver.get(url)
        driver.implicitly_wait(10)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")


            print(new_height)
            res=driver.page_source
            bsobj=BeautifulSoup(res,'html.parser')



            if 'RveJvd snByac'in str(bsobj) and '더보기' in str(bsobj):
                print('클릭')
                driver.find_element_by_css_selector(".U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ").click()
                time.sleep(2)


            if new_height == last_height:
                break

            last_height = new_height





        res=driver.page_source
        bsobj=BeautifulSoup(res,'html.parser')  

        developer=bsobj.find('a',{'class':'hrTbp R8zArc'}).text


        id=bsobj.findAll('span',{'class':'X43Kjb'})
        ids=[a.text for a in id if a.text != developer]

        bs_obj=bsobj.findAll('div',{'class':'bAhLNe kx8XBd'})
        dates=[]
        for u in bs_obj:

            date=u.findAll('span',{'class':'p2TkOb'})
            dates.append(str(date).strip('[<span class="p2TkOb">').strip('</span>]'))

        rating=bsobj.findAll('div',{'class':'nt2C1d'})
        ratings=[int(re.findall('\d+',str(c))[3]) for c in rating]

        body=bsobj.findAll('span',{'jsname':'bN97Pc'})
        bodys=[d.text for d in body]
        
        df=pd.DataFrame({'ID':ids,'Date':dates,'Rating':ratings,'Reviews':bodys})
        return df







