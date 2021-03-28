import requests
import os
import sys
import time
import argparse
import csv
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


def queryCoins(url, coinlist, date):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find("table")
    currentindex = 0
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if (currentindex > 0 and currentindex < 11):
            coinname = cells[2].find(text=True)
            price = cells[3].find(text=True)
            var24h = cells[4].find(text=True)
            var7d = cells[5].find(text=True)
            marketcap = cells[6].find(text=True)
            volumesupp = cells[7].find(text=True)
            circulatingamount = cells[8].find(text=True)
            coins = [date, coinname, price, var24h, var7d, marketcap, volumesupp, circulatingamount]
            coinlist.append(coins)
        currentindex = currentindex + 1
    return

parser = argparse.ArgumentParser()
parser.add_argument("--enddate", help="Introduce la fecha fin.")
args = parser.parse_args()
currentDir = os.path.dirname(__file__)
filename = "coins_dataset.csv"
filePath = os.path.join(currentDir, filename)
url = "https://coinmarketcap.com"
headers = ["Fecha","Moneda", "Precio", "Variación 24h", "Variación 7d", "Valor de mercado", "Volumen",
           "En circulación"]
coinlist = [headers]
enddate = datetime.strptime(args.endDate,"%d/%m/%Y")
while startdate <= enddate:
  currentdate = datetime.now()
  print ("Extrayendo datos %s" %  currentdate)
  queryCoins(url,coinlist,currentdate)
  startdate = startdate + timedelta(days = 1)
  time.sleep(60) ## Extraemos datos cada minuto

with open(filePath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for coin in coinlist:
        writer.writerow(coin)
