import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

exp_scale = 10000
min_case = 100

url= "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
html = urlopen(url)  

bsObject = BeautifulSoup(html, "html.parser") 
table = bsObject.find(class_= "js-csv-data csv-data js-file-line-container")
rows = table.select('tbody > tr')
header = table.select('th')
global ddata 

def f(x):   # The logistic function
    global ddata 
    sum=0.0
    for t in range(0,len(ddata)):
           sum = sum + (ddata[t] - (x[0]/(1+np.exp(-(x[1]+x[2]*t)/exp_scale))) )**2
    return sum

def pltdata(country):
    global ddata 
    for row in rows:
        cells = row.select('td')
        if cells[2].text == country:
            country2 = cells[2].text+" "+ cells[1].text
            for i in range(6,len(cells)-1):
                if int((cells[i].text)) > min_case :
                    ddata = [float(x.text) for x in cells[i:]]
                    result = optimize.minimize(f, [10, 10,1], method="CG")    
                 #   print(ddata)
                    print(country2, result.x)
                    #edata = [result.x[0]/(1+np.exp(-(result.x[1]+result.x[2]*t)/exp_scale))  for t in range(0,len(ddata))]
                    edata = [result.x[0]/(1+np.exp(-(result.x[1]+result.x[2]*t)/exp_scale))  for t in range(0,50)]
                    plt.plot(range(0,len(ddata)), ddata,label='dat_'+country2+"(cur:"+str(int(ddata[-1]))+")")
                    plt.plot(range(0,50), edata, linestyle=':',label='prj_'+country2+"(est:"+str(int(result.x[0]))+")")

                    inflex = -result.x[1]/result.x[2]
                    infley = result.x[0]/(1+np.exp(-(result.x[1]+result.x[2]*inflex)/exp_scale)) 

                    plt.plot(inflex, infley, 'bo')
                    plt.text(inflex+.5, infley, country2)

                    return 

def pltdata2(country,region):
    global ddata 
    for row in rows:
        cells = row.select('td')
        if (cells[2].text == country and cells[1].text == region) :
            country2 = cells[2].text+" "+ cells[1].text
            for i in range(6,len(cells)-1):
                if int((cells[i].text)) > min_case :
                    ddata = [float(x.text) for x in cells[i:]]
                    result = optimize.minimize(f, [10, 10,1], method="CG")    
                 #   print(ddata)
                    print(country2, result.x)
                    edata = [result.x[0]/(1+np.exp(-(result.x[1]+result.x[2]*t)/exp_scale))  for t in range(0,50)]
                    plt.plot(range(0,len(ddata)), ddata,label='dat_'+country2+"(cur:"+str(int(ddata[-1]))+")")
                    plt.plot(range(0,50), edata, linestyle=':',label='prj_'+country2+"(est:"+str(int(result.x[0]))+")")

                    #plt.plot(range(0,len(ddata)), edata,label='est_'+country2+"(prj:"+str(int(result.x[0]))+")")

                    inflex = -result.x[1]/result.x[2]
                    infley = result.x[0]/(1+np.exp(-(result.x[1]+result.x[2]*inflex)/exp_scale)) 

                    plt.plot(inflex, infley, 'bo')
                    plt.text(inflex+.5, infley, country2)

                    return 
pltdata("Korea, South")
pltdata("US")
pltdata("Italy")
pltdata("Japan")
pltdata("Spain")
pltdata("Germany")
#pltdata("Iran")
pltdata("Sweden")
#pltdata("Turkey")
pltdata2("United Kingdom","")
pltdata2("France","")


day3line = [min_case*2**((i/3)) for i in range(0,40)]
plt.plot(range(0,40), day3line, label='Dbl every 3d',color='k')

plt.text(30,200, 'Fit to a Logistic curve f(a,b,c;t) = a/(1+exp(b-c*t)) \nCircles: Inflextion points (t=b/c)')
lastday = str(header[-1].text)
plt.title('Logistic Regression: corona-19 confirmed cases - the day of '+str(min_case)+'th case to ' +lastday +  '\ndata: '+url + '\nfacebook.com/Heegon.Moon')

plt.yscale('log')
plt.legend()
plt.show()


