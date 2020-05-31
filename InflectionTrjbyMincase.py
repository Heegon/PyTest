
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

def dayaverage7(dat):
    ret = []
    for i in range(len(dat)-7):
        ret.append(sum(dat[i:i+7])/7.0)
    return ret


def pltdata():
    global ddata 
    global min_case
    ccmap = plt.cm.get_cmap('hsv',20)

    nsample = 45

    for row in rows:
        cells = row.select('td')
        #if (cells[2].text == country and cells[1].text == region) :
        if cells[2].text =='China': continue     
        if cells[2].text =='Korea, South': continue
        if cells[2].text =='Australia': continue
        if int((cells[-1].text)) > min_case :
            country2 = cells[2].text+" "+ cells[1].text
   
            xdata = [float(x.text) for x in cells[-nsample-8:-1]]
            ddata = dayaverage7(xdata)
            inflex=[]
            infley=[]
            #cclr = np.random.rand(3,)
            cclr = ccmap(random.randrange(0,20))
            
            cbreak = False
            
            for j in range (0,reg_days):
                        
                result = optimize.minimize(f, [10, 10,1], method="CG")    

                infl_t =  result.x[1]/result.x[2]
                
                if infl_t < -30 :
                    cbreak = True
                    break
                
                inflex.append(infl_t - nsample)
                infley.append(flogistic(result.x[0],result.x[1], result.x[2], infl_t))

                del ddata[-1]

            if cbreak == True : continue
            if cells[2].text !='Korea, South': #too flat
                plt.plot(inflex, infley, color=cclr, linestyle=':')
                plt.plot(inflex[-1], infley[-1], color=cclr,marker='.')
                #plt.plot(inflex[-1], infley[-1], color=cclr,marker='o',fillstyle='right')

            #plt.plot(inflex[0], infley[0], marker='o',color=cclr)
            plt.plot(inflex[0], infley[0], marker='o',color=cclr,markersize=0.1*np.sqrt(float(cells[-1].text)),alpha = 0.6)
            plt.plot(inflex[0], infley[0], marker='o',color=cclr,markersize=0.1*np.sqrt(infley[0]*2),alpha = 0.3)

            plt.text(inflex[0]+.1, infley[0], country2)

    return

pltdata()

plt.plot(20, 500000, marker='o',color='k',markersize=0.1*np.sqrt(1000000),fillstyle = 'none')
plt.text(20, 500000, '1000k')

plt.plot(35, 500000, marker='o',color='k',markersize=0.1*np.sqrt(100000),fillstyle = 'none')
plt.text(35, 500000, '100k')

plt.plot(40, 500000, marker='o',color='k',markersize=0.1*np.sqrt(10000),fillstyle = 'none')
plt.text(40, 500000, '10k')



plt.text(10,3000, 'circles are linear scale (by area)\nlarge: estimated max., small: current cases, dot: past wk loc.')
lastday = str(header[-1].text)
plt.title('Inflextion point 7-Day Track\nLogistic Regression: corona-19 confirmed cases\nsampling data: last 45 days (' +lastday +  ') \
(conf. cases >'+str(min_case)+' countries)\nsource: '+url + '\npython code: github.com/Heegon/PyTest')

plt.yscale('log')
plt.xlabel('Date (today=0)')
plt.ylabel('Half of max. confirmed cases (estimation) ')
#plt.legend()
plt.show()