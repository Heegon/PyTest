
#covid-19 # confirmed cases logistic regression  hgmoon68@gmail.com

import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random


#from matplotlib import font_manager, rc
#font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgunsl.ttf").get_name()
#rc('font', family=font_name)


exp_scale = 100000
min_case = int(input('Min cases to watch:'))
reg_days = 7

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


def pltdata():
    global ddata 
    global min_case
    ccmap = plt.cm.get_cmap('hsv',20)

    nsample = 30

    for row in rows:
        cells = row.select('td')
        #if (cells[2].text == country and cells[1].text == region) :
        if cells[2].text =='China': continue
        #if cells[2].text =='Peru': continue
        if int((cells[-1].text)) > min_case :
            country2 = cells[2].text+" "+ cells[1].text
   
            ddata = [float(x.text) for x in cells[-nsample-1:-1]]
            inflex=[]
            infley=[]
            #cclr = np.random.rand(3,)
            cclr = ccmap(random.randrange(0,20))
                    
            for j in range (0,reg_days):
                        
                result = optimize.minimize(f, [10, 10,1], method="CG")    

                infl_t =  result.x[1]/result.x[2]
                inflex.append(infl_t - nsample)
                infley.append(flogistic(result.x[0],result.x[1], result.x[2], infl_t))

                del ddata[-1]

            plt.plot(inflex, infley, color=cclr, linestyle=':')
            plt.plot(inflex[-1], infley[-1], color=cclr,marker='o',fillstyle='right')

            #plt.plot(inflex[0], infley[0], marker='o',color=cclr)
            plt.plot(inflex[0], infley[0], marker='o',color=cclr,markersize=10+float(cells[-1].text)/5000,alpha = 0.7)
            plt.plot(inflex[0], infley[0], marker='o',color=cclr,markersize=10+infley[0]*2/5000.,alpha = 0.3)

            plt.text(inflex[0]+.1, infley[0], country2)

    return
pltdata()

'''
day3max = 60-int(np.log10(min_case))*10
day3line = [min_case*2**((i/3)) for i in range(0,day3max)]
plt.plot(range(0,day3max), day3line, label='Dbl every 3d',color='k')
'''
plt.text(0,1000, 'circles are linear length scale (not area)\nlarge: estimated max., small: current cases, half filled: past wk loc.')
lastday = str(header[-1].text)
plt.title('Inflextion point 7-Day Track\nLogistic Regression: corona-19 confirmed cases\nsampling data: last 30 days (' +lastday +  ') \
(conf. cases >'+str(min_case)+' countries)\nsource: '+url + '\npython code: github.com/Heegon/PyTest')

plt.yscale('log')
plt.xlabel('Date (today=0)')
plt.ylabel('Half of max. confirmed cases (estimation) ')
#plt.legend()
plt.show()