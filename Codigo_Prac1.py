import csv
import os
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time

""" Esta función se encarga abrir el enlace con la web para extraer el código
    donde se encuentra la información."""

def scrapWeb(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1420,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    browser = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
    browser.get(url)
    time.sleep(60)
    browser.maximize_window()
    soup = BeautifulSoup(browser.page_source,"html.parser")
    browser.close()
    return soup

""" Esta función se encarga de extraer la información del historial de 
    la criptomoneda y almacenarla en una lista. """

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

# Transforma la fecha al formato dd/mm/yyyy.

def mdy_to_ymd(d):
     return datetime.strptime(d, '%b %d, %Y').strftime('%d/%m/%Y')

"""Esta función se encarga de buscar los enlaces del historial de las criptomonedas de la página principal. """

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

# Esta función guarda el histórico de la criptomoneda en un archivo .CSV.

def writeCSV(coinhistory,coinname):
    print("Escribiendo histórico de la criptomoneda " +coinname)
    currentDir = os.path.dirname(__file__)
    date = datetime.today().strftime('%Y-%m-%d')
    filename = coinname + "-" + date + ".csv"
    filePath = os.path.join(currentDir, "CoinsCSV", filename)
    with open(filePath, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for field in coinhistory:
            writer.writerow(field)

# Main del programa.

if not os.path.exists('CoinsCSV'):
    os.makedirs('CoinsCSV')
queryCoins("https://coinmarketcap.com")
