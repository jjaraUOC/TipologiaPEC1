import csv
import os
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrapWeb(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,"html.parser")
    return soup

def coinHistorical(url_historical):
    headers = ["Fecha","Open", "High", "Low", "Close", "Volumen", "Market_Cap"]
    coinlist = [headers]
    soup = scrapWeb(url_historical)
    tabla = soup.find("table")
    for row in tabla.find_all("tr"):
        cell = row.find_all("td")
        if (len(cell) == 7):
            Fecha = mdy_to_ymd(cell[0].find(text=True))
            Open = cell[1].find(text=True)
            High = cell[2].find(text=True)
            Low =  cell[3].find(text=True)
            Close = cell[4].find(text=True)
            Volumen = cell[5].find(text=True)
            Market_Cap = cell[6].find(text=True)
            coins = [Fecha, Open, High, Low, Close, Volumen, Market_Cap]
            coinlist.append(coins)
    return coinlist

def mdy_to_ymd(d):
     return datetime.strptime(d, '%b %d, %Y').strftime('%d/%m/%Y')    


def queryCoins(url):
    soup = scrapWeb(url)
    table = soup.find("table")
    count = 0
    link_coin = ""
    coinName = ""
    for row in table.findAll("tr"):
        count = count + 1
        coins = row.findAll("td")
        for cell in coins:
            if count <= 10:
                item_ref = cell.find('div', {"class": "sc-AxhCb bXGzHn"})
                if (item_ref is not None):
                    item = item_ref.find('a')
                    link_coin = "https://coinmarketcap.com" + item['href'] + "historical-data"
            else:
                item_ref = cell.find('a')
                if item_ref is not None:
                    link_coin = "https://coinmarketcap.com" + item_ref['href'] + "historical-data"
        if(link_coin == ""): continue
        coinName = coins[2].find(text=True)
        writeCSV(coinHistorical(link_coin), coinName)
        time.sleep(60)

def writeCSV(coinhistory,coinname):
    print("Escribiendo histórico de la criptomoneda " +coinname)
    currentDir = os.path.dirname(__file__)
    date = datetime.today().strftime('%Y-%m-%d')
    filename = coinname + "-" + date +" .txt"
    filePath = os.path.join(currentDir, "CoinsCSV", filename)
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for field in coinhistory:
            writer.writerow(field)


chrome_options = Options()
chrome_options.add_argument("--headless") ## Con esta linea nos aseguramos que el navegador de Chrome no abra una nueva pestaña.
browser = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
if not os.path.exists('CoinsCSV'):
    os.makedirs('CoinsCSV')
queryCoins("https://coinmarketcap.com")


browser.close()




    


        
   
    
