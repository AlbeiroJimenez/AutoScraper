from datetime import datetime
from datetime import timedelta
import time, re
import pandas as pd
from threading import Thread
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from spyder import Spyder

FACEBOOK      = ['yourfacebookaccount', 'password']
NAMES_CLASSES = {'adsURL':'x3ct3a4', 'titleAd':'x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 xw06pyt xngnso2 x1qb5hxa x1xlr1w8 xzsf02u', 
                 'price':'x1xmf6yo', 'geoDate':'x1yztbdb', 'description':'x126k92a xkhd6sd xsag5q8 x4uap5 xz9dl7a'
                }
RECORDS_SAVE  = 10
DELAY_TIME    = 30


class Crawler:
    def __init__(self):
        self.spyder     = Spyder()
        self.stop       = False
        self.urlMarket  = None
        self.ads        = []
        
    def makeCrawling(self):
        pass

class OlxCrawler(Crawler):
    def __init__(self):
        super().__init__()
    
    def makeCrawling(self):
        self.spyder.setDriver('https://www.olx.com.pe/autos_c378?filter=condition_eq_2')
        while self.spyder.existWebElement('XPATH', '//button/span[contains(text(), "cargar más")]'):
            loadPlus, errorLoadPlus = self.spyder.getWebElement('XPATH', '//button/span[contains(text(), "cargar más")]')
            loadPlus[0].click()
        
class MercadoLibreCrawler(Crawler):
    def __init__(self):
        super().__init__()

class FacebookCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.urlMarket = ['https://www.facebook.com/marketplace/trujillo/carros/?minPrice=1000&itemCondition=used&exact=false', 
                          'https://www.facebook.com/marketplace/lima/carros?minPrice=1000&itemCondition=used&exact=false', 
                          'https://www.facebook.com/marketplace/109507649080609/carros/?minPrice=1000&itemCondition=used&exact=false'
                          ]
        self.urlAds    = []
        self.codeWeb   = 1
        self.market    = 'Facebook Marketplace'
        self.database  = []
        
    def makeCrawling_threaded(self, nameDatabase, region=0):
        thread = Thread(target=self.makeCrawling, args=(nameDatabase, region,))
        thread.start()
        
    def makeCrawling(self, nameDatabase, region):
        self.database  = []
        for region in self.urlMarket[region:region+1]:
            #self.spyder.setDriver(region)
            #links, linksError = self.spyder.getWebElement('XPATH', '//div[@class="sonix8o1"]')
            links, linksError = self.spyder.getWebElement('XPATH', '//div[@class="%s"]'%NAMES_CLASSES['adsURL'])
            print(len(links))
            for link in links:
                try:
                    urlAd = urlparse(link.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))
                    if 'item' in urlAd.path:
                        self.urlAds.append(urlAd.geturl())
                except:
                    print('No agregado')
            cont = 0
            for urlAd in self.urlAds:
                print(cont)
                cont += 1
                if self.stop == True: break
                try:
                    facebookId = urlparse(urlAd).path.split('/')[-2]
                    self.spyder.setDriver(urlAd)
                    #image, imageError = self.spyder.getWebElement('XPATH', '//img[contains(@alt,"auto") or contains(@alt,"Auto") or contains(@alt,"carro")]', timeout_=10, max_iteractions=3)
                    #if image == -1: continue
                    title, titleError = self.spyder.getWebElement('XPATH','//span[contains(@class, "%s")]'%NAMES_CLASSES['titleAd'])
                    if title == -1 or len(title)<2: continue
                    marca = title[1].get_attribute('textContent')
                    try:
                        year = re.findall(r'\d{4}|\d{2}', marca)[0]
                    except:
                        year = ''
                    rawPrice, error = self.spyder.getWebElement('XPATH','//div[@class="%s"]'%NAMES_CLASSES['price'])
                    if rawPrice == -1: continue
                    price = re.findall(r'-?\d+\.?\d*', rawPrice[0].get_attribute('textContent'))[0]
                    currency = rawPrice[0].get_attribute('textContent').replace(price,'')
                    geoDate, error = self.spyder.getWebElement('XPATH','//div[@class="%s"]'%NAMES_CLASSES['geoDate'])
                    if geoDate == -1: continue
                    city, department = geoDate[1].find_element(By.TAG_NAME,'a').get_attribute('textContent').split(',')
                    date = geoDate[1].get_attribute('textContent').replace(geoDate[1].find_element(By.TAG_NAME,'a').get_attribute('textContent'),'').replace(' en ', '')
                    days = self.calcDays(date)
                    published = self.calcDate(days)
                    watchPlus, error = self.spyder.getWebElement('XPATH', '//span[contains(text(),"Ver más")]', timeout_=0)
                    if watchPlus != -1: watchPlus[0].click()
                    #Description Element
                    webElement, error = self.spyder.getWebElement('XPATH', '//div[contains(@class,"%s")]'%NAMES_CLASSES['description'])
                    if webElement != -1:
                        description = webElement[0].get_attribute('textContent')
                    else:
                        description = ''
                    try:
                        rawPrice = re.findall(r'\d*\,?\d*\ *usd\ *\$*\ *\d*\,?\d*', description.casefold())[0]
                    except:
                        rawPrice = ''
                    if rawPrice != '':
                        currency_ = re.findall(r'usd', rawPrice.casefold())
                        currency  = currency_[0] if currency_ != [] else currency 
                        price_ = re.findall(r'\d+\,?\d*', rawPrice.casefold())
                        price  = price_[0] if price_ != [] else price
                    try:
                        rawYear = re.findall(r'modelo\ *\d{2,4}|año\ *\d{2,4}|fabricación\ *\d{2,4}|fabricacion\ *\d{2,4}', description.casefold())[0]
                    except:
                        rawYear = ''
                    if rawYear != '':
                        year_ = re.findall(r'\d{2,4}', rawYear.casefold())
                        year  = year_[0] if year_ != [] else year
                    item = {
                        'Fecha Publicación': published, 
                        'Tiempo de publicación activa (días)': days, 
                        'Sitio Web': self.market, 
                        'Código Web': self.codeWeb,
                        'Marca': marca,
                        'ID Marca': '',
                        'Modelo': '',
                        'ID Modelo': '',
                        'Año de Fabricación': year,
                        'Ciudad': city,
                        'Departamento': department,
                        'ID Departamento': '',
                        'Región': '',
                        'ID Región': '',
                        'Moneda': currency,
                        'Valor': price,
                        'ID Publicación': facebookId,
                        'Texto Anuncio': description
                    }  
                    self.database.append(item) 
                    time.sleep(DELAY_TIME)
                    print(item) 
                except:
                    print('No agregado 2')
                if cont%RECORDS_SAVE == 0 and cont>0:
                    dataToSave = pd.DataFrame(self.database)
                    dataToSave.to_excel(nameDatabase)
            dataToSave = pd.DataFrame(self.database)
            dataToSave.to_excel(nameDatabase)
    
    def calcDate(self, days):
        try:
            days = float(days)
        except:
            return days
        newDate = datetime.now()-timedelta(days=days)
        return newDate.strftime('%d/%m/%Y')
                
    def calcDays(self, text):
        text = text.casefold()
        if 'minuto' in text:
            return '0'
        elif 'horas' in text:
            return str(int(re.findall(r'-?\d+\.?\d*', text)[0])/24)
        elif 'hora' in text:
            return '0'
        elif 'días' in text or 'dias' in text:
            return re.findall(r'-?\d+\.?\d*', text)[0]
        elif 'día' in text or 'dia' in text:
            return '1'
        elif 'semanas' in text:
            return str(int(re.findall(r'-?\d+\.?\d*', text)[0])*7)
        elif 'semana' in text:
            return '7'
        elif 'meses' in text:
            return str(int(re.findall(r'-?\d+\.?\d*', text)[0])*30)
        elif 'mes' in text:
            return '30'
        elif 'años' in text:
            return str(int(re.findall(r'-?\d+\.?\d*', text)[0])*365)
        elif 'año' in text:
            return '365'
        else:
            return text    
    
    def makeScrollEnd(self):
        scroll   = True
        scroller = 0
        self.loginFacebook()
        self.spyder.setDriver('https://www.facebook.com/marketplace/trujillo/carros/?minPrice=1000&itemCondition=used&exact=false')
        time.sleep(5)
        links, error = self.spyder.getWebElement('XPATH', '//div[@class="sonix8o1"]')
        link = links[-1].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        while scroll:
            self.spyder.scrollDown()
            scroller += 1
            if scroller%15 == 0:
                time.sleep(5)
                links, error = self.spyder.getWebElement('XPATH', '//div[@class="sonix8o1"]')
                if link == links[-1].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'):
                    scroll = False
                else:
                    link = links[-1].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        print(len(links))
        #pixelId = re.findall(r'-?\d+\.?\d*', pixel[0].get_attribute('title'))[0]
        
        print('Hemos terminado de desplegar todos los resultados')
        
    def loginFacebook(self):
        self.spyder.setDriver('https://www.facebook.com/login/')
        email, errorEmail = self.spyder.getWebElement('XPATH', '//input[@id="email"]')
        email[0].send_keys(FACEBOOK[0])
        passwd, errorPasswd = self.spyder.getWebElement('XPATH', '//input[@id="pass"]')
        passwd[0].send_keys(FACEBOOK[1])
        submit, errorSubmit = self.spyder.getWebElement('XPATH', '//button[@id="loginbutton"]')
        submit[0].click()
        
class KavakCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.urlMarket = 'https://www.kavak.com/pe/orden-menor-precio/carros-usados'
        
    def makeCrawling(self):
        self.spyder.setDriver(self.urlMarket)
        #market, marketError = self.spyder.getWebElement('XPATH', '//button/div[contains(text(),"Seguir en")]')
        #if market != -1: market[0].click()
        time.sleep(5)
        pages, pagesError = self.spyder.getWebElement('XPATH', '//div/span[@class="total"]')
        if pages != -1: pages = int(pages[0].text)
        dataLayer = self.spyder.driver.execute_script('return dataLayer')
        for data in dataLayer:
            if data['event'] == 'ProductImpression':
                for ad in data['ecommerce']['impressions']:
                    self.ads.append(ad)
        for page in range(2,pages+1):
            pageURL = 'https://www.kavak.com/pe/page-%s/orden-menor-precio/carros-usados'%str(page)
            self.spyder.setDriver(pageURL)
            time.sleep(5)
            dataLayer = self.spyder.driver.execute_script('return dataLayer')
            for data in dataLayer:
                if data['event'] == 'ProductImpression':
                    for ad in data['ecommerce']['impressions']:
                        self.ads.append(ad)
    
    def getBaseKavak(self):
        for index in range(len(self.ads)):
            color, mileage, transmission, year = self.ads[index]['variant'].split(',')
            self.ads[index]['Color'] = color
            self.ads[index]['Mileage'] = mileage
            self.ads[index]['transmission'] = transmission
            self.ads[index]['year'] = year   
        database = pd.DataFrame(self.ads)
        database.to_excel('MarketplaceKavak.xlsx')

if __name__ == '__main__':
    facebook = FacebookCrawler()
    kavak = KavakCrawler()
