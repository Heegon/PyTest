import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgunsl.ttf").get_name()
rc('font', family=font_name)


exp_scale = 10000
min_case = 1000

url= "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
html = urlopen(url)  

bsObject = BeautifulSoup(html, "html.parser") 
table = bsObject.find(class_= "js-csv-data csv-data js-file-line-container")
rows = table.select('tbody > tr')
header = table.select('th')
global ddata 


def flogistic(a,b,c,t): # The logistic function
    return a/(1+np.exp( (b-c*t)/exp_scale) )

def f(x):   # cost function
    global ddata 
    sum=0.0
    for t in range(0,len(ddata)):
           sum = sum + (ddata[t] - flogistic(x[0],x[1],x[2],t))**2
    return sum


def pltdata2(country,region):
    global ddata 
    for row in rows:
        cells = row.select('td')
        if (cells[2].text == country and cells[1].text == region) :
            country2 = cells[2].text+" "+ cells[1].text
            for i in range(6,len(cells)):
                if int((cells[i].text)) > min_case :
                    ddata = [float(x.text) for x in cells[i:]]
                    result = optimize.minimize(f, [10, 10,1], method="CG")    

                    print(country2, result.x)
                    
                    cclr = np.random.rand(3,)
                    
                    edata = [flogistic(result.x[0],result.x[1], result.x[2], t)  for t in range(0,50)]
                    plt.plot(range(0,len(ddata)), ddata, color=cclr, label='dat_'+country2+"(cur:"+str(int(ddata[-1]))+")")
                    plt.plot(range(0,50), edata, color=cclr, linestyle=':',label='prj_'+country2+"(est:"+str(int(result.x[0]))+")")

                    inflex = result.x[1]/result.x[2]
                    infley = flogistic(result.x[0],result.x[1], result.x[2], inflex)

                    plt.plot(inflex, infley, 'bo')
                    plt.text(inflex+.5, infley, country2)

                    return 

pltdata2("Korea, South","")
pltdata2("US","")
#pltdata2("China","Hubei")
pltdata2("Japan","")
pltdata2("Italy","")
pltdata2("Spain","")
pltdata2("Germany","")
pltdata2("Sweden","")
pltdata2("United Kingdom","")
pltdata2("France","")
pltdata2("Iran","")
pltdata2("Turkey","")
pltdata2("Israel","")

day3max = 60-int(np.log10(min_case))*10
day3line = [min_case*2**((i/3)) for i in range(0,day3max)]
plt.plot(range(0,day3max), day3line, label='Dbl every 3d',color='k')

plt.text(30,2*min_case, 'Fit to a Logistic curve f(a,b,c;t) = a/(1+exp(b-c*t)) \nCircles: Inflextion points (t=b/c)\
\n※Caution:Error can be larger if the inflextion point has not arrived')
lastday = str(header[-1].text)
plt.title('Logistic Regression: corona-19 confirmed cases - the day of '+str(min_case)+'th case to ' +lastday +  '\ndata: '+url + '\nfacebook.com/Heegon.Moon')

plt.yscale('log')
plt.legend()
plt.show()


