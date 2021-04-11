<H1>Extracción del histórico de criptomonedas mediante Web Scrapping</H1>

El trabajo consiste en la extracción del histórico de las 100 criptomonedas más relevantes 
de la web  [Coin Market Cap](https://coinmarketcap.com).

Este histórico, será almacenado en un *.csv* (Comma Separated Values) para un posible análisis posterior.


<h3>Miembros del equipo</h3> 

* *José Antonio Jara*

* *Óscar López Montero*

<h3>Pasos previos</h3> 

Previa a la ejecución del programa, es necesario instalar las siguientes dependencias:

**Beautifulsoup**
>pip install beautifulsoup4

**Selenium**
>pip install selenium

**Html5lib**
>pip install html5lib

**Fake_useragent**
>pip install fake_useragent

Aparte de las dependencias, el sistema desde el que se ejecuta el script debe de tener instalado
**Google Chrome (ver. 89)**. 

Esto es debido a que nuestro scrapper hace un uso combinado de Selenium 
y BeautifulSoup con el fin de extraer los históricos de cada moneda de la manera más 
óptima posible.

<h3>Funcionamiento</h3> 

El funcionamiento del Scrapper es el siguiente:

1. Se recorren todas las monedas contenidas en [CoinMarketCap](https://coinmarketcap.com) con el fin de extraer
su dirección y acceder a su histórico
2. El script accede a la dirección correspondiente a cada moneda.
3. Se recogen los datos contenidos en el histórico de la moneda en cuestión.
4. Se escriben los datos en un fichero .csv, junto al nombre de la moneda y la fecha en la que fueron
recogidos.
