import csv
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrapWeb(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,"html5lib")
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
            
            coins = [Fecha, Open, High, Low, Close, volumen, Market_Cap]
            coinlist.append(coins)
            
def mdy_to_ymd(d):
     return datetime.strptime(d, '%b %d, %Y').strftime('%d/%m/%Y')    


def queryCoins(url):
    soup = scrapWeb(url)
    table = soup.find("table")
    count = 0
    for row in table.findAll("tr"):
        count = count + 1
        for cell in row.findAll("td"):
            if count <= 10:
                item_ref = cell.find('div', {"class": "sc-AxhCb bXGzHn"})        
                if (item_ref is not None):
                    item = item_ref.find('a')
                    link_coin = "https://coinmarketcap.com" + item['href'] + "historical-data"
                    coinHistorical(link_coin)
            else:
                item_ref_2 = cell.find('a')
                if item_ref_2 is not None:          
                    link_coin_2 = "https://coinmarketcap.com" + item_ref_2['href'] + "historical-data"
                    print(link_coin_2)

def writeCSV(conlist):
    currentDir = os.path.dirname(__file__)
    filename = "coins_dataset.csv"
    filePath = os.path.join(currentDir, filename)
    with open(filePath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for coin in coinlist:
        writer.writerow(coin)


chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)     

queryCoins("https://coinmarketcap.com")


browser.close()




    


        
   
    