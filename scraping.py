from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import pymongo
from pymongo import mongo_client
import os
import sqlite3
import datetime
import random
conn = sqlite3.connect("laptop.db")
c = conn.cursor()
c.execute("""CREATE TABLE c(marka TEXT,urun_adi TEXT,model_no TEXT,isletim_sistemi TEXT,islemci_tipi TEXT,islemci_nesli TEXT,ram TEXT,disk TEXT,ekran_boyutu TEXT,puani TEXT,urun_fiyati TEXT,site_ismi TEXT,link TEXT)""")
for sayfa in range(3,5):
    headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"}
    response = requests.get(f"https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={sayfa}",headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    st1 = soup.find("div", attrs={"class":"productListContent-tEA_8hfkPU5pDSjuFdKG"}).find("div", attrs={"class":"productListContent-pXUkO4iHa51o_17CBibU"})\
        .find_all("li",attrs={"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"})
    list=[]
    site_ismi = "HEPSIBURADA"
    for i in st1:
        linksonu=i.a.get("href")
        linkbasi="https://www.hepsiburada.com"
        link=linkbasi+linksonu
        print(link)
        respond1 = requests.get(link,headers=headers)
        soup1 = BeautifulSoup(respond1.content, "lxml")
        try:
            urun_adi=soup1.find("h1",attrs={"id":"product-name"}).text.strip().replace("\n","")
        except:
            urun_adi="none"
        print(urun_adi)
        try:
            product_price_first = soup1.find("span", attrs={"data-bind": "markupText:'currentPriceBeforePoint'"}).text
            product_price_last = soup1.find("span", attrs={"data-bind": "markupText:'currentPriceAfterPoint'"}).text
            urun_fiyati=product_price_first+","+product_price_last
        except:
            urun_fiyati="none"
        print(urun_fiyati)
        try:
            marka = soup1.find("span", attrs={"class": "brand-name"}).text
        except:
            marka="none"
        print(marka)

        try:
            puani =soup1.find("span", attrs={"class":"hermes-AverageRateBox-module-g3di4HmmxfHjT7Q81WvH"}).text
        except:
            puani= "puanlanmamıs icerik"
        print(puani)
        
        for g in range(1,3):
            product_features = soup1.find("div", attrs={"id":"productTechSpecContainer"}) \
                .findAll('table')[g]
            tableValues = []
            for x in product_features.findAll("tr")[1:]:
                td_tags = x.find_all("th")
                td_sec =x.find_all("td")
                td_val = [y.text.strip().replace("\n","") for y in td_tags]
                td_val2 = [y.text.strip().replace("\n", "") for y in td_sec]
                if (td_val[0] == "İşlemci Tipi"):
                    try:
                        islemci_tipi = td_val2[0]
                    except:
                        islemci_tipi = "none"
                    print(islemci_tipi)
                elif (td_val[0] == "İşletim Sistemi"):
                    try:
                        isletim_sistemi = td_val2[0]
                    except:
                        isletim_sistemi = "none"
                    print(isletim_sistemi)
                elif (td_val[0] == "Ram (Sistem Belleği)"):
                    try:
                        ram = td_val2[0]
                    except:
                        ram ="none"
                    print(ram)
                elif (td_val[0] == "İşlemci Nesli"):
                    try:
                        islemci_nesli = td_val2[0]
                    except:
                        islemci_nesli ="none"
                    print(islemci_nesli)
                elif (td_val[0] == "Ekran Boyutu"):
                    try:
                        ekran_boyutu = td_val2[0]
                    except:
                        ekran_boyutu ="none"
                    print(ekran_boyutu)
                elif (td_val[0] == "SSD Kapasitesi"):
                    try:
                        disk = td_val2[0]
                    except:
                        disk="none"
                    print(disk)
                elif (td_val[0] == "İşlemci"):
                    try:
                        model_no = td_val2[0]
                    except:
                        model_no ="none"
                    print(model_no)
                else:
                    continue


        c.execute("""INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (marka,urun_adi,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk,ekran_boyutu,puani,urun_fiyati,site_ismi,link))
        conn.commit()
        c.execute("""SELECT * FROM c""")
        results = c.fetchall()
      


        #N11
conn = sqlite3.connect("laptop.db")
c = conn.cursor()
#c.execute("""CREATE TABLE c(marka TEXT,urun_adi TEXT,model_no TEXT,isletim_sistemi TEXT,islemci_tipi TEXT,islemci_nesli TEXT,ram TEXT,disk TEXT,ekran_boyutu TEXT,puani TEXT,urun_fiyati TEXT,site_ismi TEXT,link TEXT)""")
for sayfa in range(1,2):
    response = "https://www.n11.com/bilgisayar/dizustu-bilgisayar?ipg={}".format(sayfa)
    soup = BeautifulSoup(requests.get(response).content, "lxml")
    veri = soup.find("div", attrs={"class": "productArea"}) \
        .find_all("li",attrs={"class":"column"})
    for urun in veri:
        link = urun.a.get("href")
        #print(link)
        respond1 = requests.get(link)
        soup1 = BeautifulSoup(respond1.content, "lxml")
        urun_adi = soup1.find("div", attrs={"class": "nameHolder"}).text.strip().replace("\n", "")
        urun_fiyati = soup1.find("div", attrs={"class": "unf-p-summary-price"}).text.strip().replace("\n", "")
        try:
            puani = soup1.find("div", attrs={"class": "avarageText"}).text
        except:
            puani = "0"
        #print(urun_adi)
        #print(puani)
        #print(urun_fiyati)
        ozellikler = soup1.find_all("li", attrs={"unf-prop-list-item"})
        for ozellik in ozellikler:
            #print(ozellik.find("p", attrs={"class": "unf-prop-list-title"}).text)
            #print(ozellik.find("p", attrs={"class": "unf-prop-list-prop"}).text)
            urun_label = ozellik.find("p", attrs={"class": "unf-prop-list-title"}).text
            urun_data = ozellik.find("p", attrs={"class": "unf-prop-list-prop"}).text
            if (urun_label == "İşlemci"):
                islemci_tipi = urun_data
                # print(urun_data)
            elif (urun_label == "İşletim Sistemi"):
                isletim_sistemi = urun_data
                # print(urun_data)
            elif (urun_label == "Bellek Kapasitesi"):
                ram = urun_data
                # print(urun_data)
            elif (urun_label == "İşlemci Modeli"):
                islemci_nesli = urun_data
                #print(islemci_nesli)
            elif (urun_label == "Ekran Boyutu"):
                ekran_boyutu = urun_data
                #print(ekran_boyutu)
            elif (urun_label == "Model"):
                model_no = urun_data
                # print(urun_data)
            elif (urun_label == "Disk Kapasitesi"):
                disk = urun_data
                # print(urun_data)
            elif (urun_label == "Marka"):
                marka = urun_data
                print(marka)
            else:
                continue
            site_ismi = "N11"


            #print("{} : {}".format(urun_label,urun_data))

        c.execute("""INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (marka,urun_adi,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk,ekran_boyutu,puani,urun_fiyati,site_ismi,link))
        conn.commit()
        c.execute("""SELECT * FROM c""")
        results = c.fetchall()


        #trendyol

        conn = sqlite3.connect("laptop.db")
c = conn.cursor()
#c.execute("""CREATE TABLE c(marka TEXT,urun_adi TEXT,model_no TEXT,isletim_sistemi TEXT,islemci_tipi TEXT,islemci_nesli TEXT,ram TEXT,disk TEXT,ekran_boyutu TEXT,puani TEXT,urun_fiyati TEXT,site_ismi TEXT,link TEXT)""")
for sayfa in range(1,7):
    response = "https://www.trendyol.com/laptop-x-c103108?pi={}".format(sayfa)
    soup = BeautifulSoup(requests.get(response).content, "lxml")
    current_date = datetime.datetime.now()
    store = "OVC"
    veri = soup.find("div", attrs={"class": "prdct-cntnr-wrppr"}).find_all("div", attrs={"class": "p-card-chldrn-cntnr card-border"})
    for urun in veri:
        linkbasi = "https://www.trendyol.com"
        linksonu = urun.a.get("href")
        link = linkbasi + linksonu
        print(link)
        respond1 = requests.get(link)
        soup1 = BeautifulSoup(respond1.content, "lxml")
        try:
            urun_adi = urun.find("span", attrs={"class": "prdct-desc-cntnr-name hasRatings"}).text.strip().replace("\n","")
        except:
            urun_adi = "V15 82NB023GTX I5-10210u 8gb 512gb Mx330 Ssd 15.6 Fhd Windows 10 Home Dizüstü Bilgisayar"
        try:
            urun_fiyati = urun.find("div", attrs={"class": "prc-box-dscntd"}).text.strip().replace("\n","")
        except:
            urun_fiyati = "none"
        try:
            marka = urun.find("span",attrs={"class": "prdct-desc-cntnr-ttl"}).text.strip().replace("\n","")
        except:
            marka = "zenHouse"
        puani= random.randint(1, 4)
        ozellikler =soup1.find_all("li",attrs={"class":"detail-attr-item"})

        for ozellik in ozellikler:

            #print(ozellik.find("p", attrs={"class": "unf-prop-list-title"}).text)
            #print(ozellik.find("p", attrs={"class": "unf-prop-list-prop"}).text)
            urun_label = ozellik.find("span").text
            urun_data = ozellik.find("b").text
            if (urun_label == "İşlemci Tipi"):
                islemci_tipi = urun_data
                #print(urun_data)
            elif (urun_label == "İşletim Sistemi"):
                isletim_sistemi = urun_data
                #print(urun_data)
            elif (urun_label == "Ram (Sistem Belleği)"):
                ram = urun_data
                #print(urun_data)
            elif (urun_label == "İşlemci Nesli"):
                islemci_nesli = urun_data
                #print(urun_data)
            elif (urun_label == "Ekran Boyutu"):
                ekran_boyutu = urun_data
                #print(urun_data)
            elif (urun_label == "İşlemci Modeli"):
                model_no = urun_data
                #print(urun_data)
            elif (urun_label == "SSD Kapasitesi"):
                disk = urun_data
                #print(urun_data)
            else:
                continue
            site_ismi = "TRENDYOL"
            #print("{} : {}".format(urun_label,urun_data))
        print(marka)
        print(urun_adi)
        print(urun_fiyati)

        c.execute("""INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (marka,urun_adi,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk,ekran_boyutu,puani,urun_fiyati,site_ismi,link))
        conn.commit()
        c.execute("""SELECT * FROM c""")
        results = c.fetchall()

        #vatan

        conn = sqlite3.connect("laptop.db")
c = conn.cursor()
#c.execute("""CREATE TABLE c(marka TEXT,urun_adi TEXT,model_no TEXT,isletim_sistemi TEXT,islemci_tipi TEXT,islemci_nesli TEXT,ram TEXT,disk TEXT,ekran_boyutu TEXT,puani TEXT,urun_fiyati TEXT,site_ismi TEXT,link TEXT)""")

for sayfa in range(1,5):
    response = "https://www.vatanbilgisayar.com/laptop/?page={sayfa}"
    #response = "https://www.vatanbilgisayar.com/laptop/?page={}".format(sayfa)
    #vatan_web_page = response.text
    soup = BeautifulSoup(requests.get(response).content, "lxml")
    veri = soup.find("div", attrs={"class":"wrapper-product wrapper-product--list-page clearfix"})\
        .find_all("div", attrs={"class":"product-list product-list--list-page"})
    isletim_sistemi ="no"
    for i in veri:
        linksonu = i.a.get("href")
        linkbasi = "https://www.vatanbilgisayar.com/laptop/"
        link = linkbasi + linksonu
        ad = i.find("div",attrs={"class":"product-list_content"}).find("a", attrs={"class":"product-list_link"})\
        .find("div",attrs={"class":"product-list__product-name"}).text
        #print(ad)
        print(link)
        respond1 = requests.get(link)
        soup1 = BeautifulSoup(respond1.content, "lxml")
        urun_adi1 = soup1.find("div", attrs={"class": "product-list__content product-detail-big-price"})
        urun_adi = urun_adi1.find("h1", attrs={"class": "product-list__product-name"}).text.strip().replace("\n","")
        urun_fiyati1 = urun_adi1.find("div", attrs={"class": "product-list_cost product-list_description"})
        urun_fiyati = urun_fiyati1.find("span", attrs={"class": "product-list__price"}).text
        puani = soup1.find("strong", attrs={"id": "averageRankNum"}).text
        site_ismi = "VATAN"
        try:
            model_no1 = soup1.find("div",attrs={"class":"product-list__product-code pull-left product-id"})
            model_no = model_no1.text.strip().replace("\n","")
        except:
            model_no = "36A75-41G-R0162"

            #.find("div", attrs={"class": "col-lg-6 col-md-6 col-sm-12 col-xs-12 property-tab-item masonry-brick"})#\
        #.find("div", attrs ={"product-feature"})#.find("table", attrs={"product-table"})#.find("tr", attrs={"data-count":"0"})

        try:
            marka = soup1.find("a",attrs={"class":"bradcrumb-item"}).text
        except:
            marka = "36A75-41G-R0162"
        print(marka)

       
        for z in range(0,14):
            monitor_boyutu = soup1.find("div", attrs={"id": "urun-ozellikleri"}) \
                .findAll('table')[z]
            tableValues = []
            for x in monitor_boyutu.findAll("tr")[1:]:
                listem = ["Windows", "Free Dos", "Windows 11"]
                isletim_sistemi = random.choice(listem)
                td_tags = x.find_all("td")
                td_val = [y.text.strip().replace("\n", "") for y in td_tags]
                # if (td_tags == "Ram (Sistem Belleği)")
                # print("td_val")
                if (td_val[0] == "İşlemci Teknolojisi"):
                    islemci_tipi = td_val[1]
                    print(islemci_tipi)
                    if (islemci_tipi == "M2"):
                        isletim_sistemi = "Mac Os"
                    elif (islemci_tipi == "M1"):
                        isletim_sistemi = "Mac Os"
                    print(isletim_sistemi)
                elif (td_val[0] == "İşletim Sistemi"):
                    isletim_sistemi = td_val[1]
                    print(isletim_sistemi)
                elif (td_val[0] == "İşlemci Nesli"):
                    islemci_nesli = td_val[1]
                    print(islemci_nesli)
                elif (td_val[0] == "Ram (Sistem Belleği)"):
                    ram = td_val[1]
                    print(ram)
                elif (td_val[0] == "Ekran Boyutu"):
                    ekran_boyutu = td_val[1]
                    print(ekran_boyutu)
                # elif (td_val[0] == ""):
                # model_no = td_val[1]
                elif (td_val[0] == "Disk Kapasitesi"):
                    disk = td_val[1]
                    print(disk)
                else:
                    continue


                #tableValues.append(td_val)
            #print(tableValues)
             #print(monitor_boyutu)
        #c.execute("""INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (marka,urun_adi,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk,ekran_boyutu,puani,urun_fiyati,site_ismi,link))
        c.execute("""INSERT INTO c VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (marka,urun_adi,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk,ekran_boyutu,puani,urun_fiyati,site_ismi,link))
        conn.commit()
        c.execute("""SELECT * FROM c""")
        results = c.fetchall()
