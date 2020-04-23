#covid-19 # confirmed cases logistic regression  hgmoon68@gmail.com

import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
from cycler import cycler


#from matplotlib import font_manager, rc
#font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgunsl.ttf").get_name()
#rc('font', family=font_name)


exp_scale = 100000
min_case = 1000
reg_days = 7
parm_90= np.log(1/0.9 - 1) * exp_scale

url= "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
html = urlopen(url)  

bsObject = BeautifulSoup(html, "html.parser") 
table = bsObject.find(class_= "js-csv-data csv-data js-file-line-container")
rows = table.select('tbody > tr')
header = table.select('th')

global ddata 
global ccount 
ccount = 0

new_colors = ['b', '#ff7f0e', '#2ca02c', '#d62728',  #'#1f77b4'
              '#9467bd', '#8c564b', '#e377c2', '#dd1c77',
              '#31a354', '#17becf', '#fdae6b', '#756bb1']

def flogistic(a,b,c,t): # The logistic function

    time_sclae = t # log-logistic np.log(t)
    return a/(1+np.exp( (b-c*time_sclae)/exp_scale) )

def f(x):   # cost function
    global ddata 
    sum=0.0
    for t in range(0,len(ddata)):            
           sum = sum + (ddata[t] - flogistic(x[0],x[1],x[2],t))**2
    return sum


def pltdata2(country,region):
    global ddata 
    global ccount 

    for row in rows:
        cells = row.select('td')
        if (cells[2].text == country and cells[1].text == region) :
            country2 = cells[2].text+" "+ cells[1].text
            for i in range(6,len(cells)):
                if int((cells[i].text)) > min_case :

                    ddata = [float(x.text) for x in cells[i:]]
                    #if cells[2].text == 'US' : ddata[33] = 585909 #04-14 typo error
                    nsample = len(ddata)
                    inflex=[]
                    infley=[]
                    #cclr = np.random.rand(3,)
                    #cclr = ccmap(random.randrange(0,20))
                    cclr = new_colors[ccount]
                    if ccount < len(new_colors)-1  :
                        ccount += 1
                    else:
                        ccount = 0
                    
                    for j in range (0,reg_days):
                        
                        result = optimize.minimize(f, [10, 10,1], method="CG")    

                        inflex.append( result.x[1]/result.x[2])
                        infley.append(flogistic(result.x[0],result.x[1], result.x[2], inflex[-1]))

                        if j==0: # data and projection plot
                            edata = [flogistic(result.x[0],result.x[1], result.x[2], t)  for t in range(0,50)]
                            plt.plot(range(0,len(ddata)), ddata, color=cclr, linewidth = 0.7, label='dat_'+country2+"(cur:"+str(int(ddata[-1]))+")")
                            plt.plot(range(0,50), edata, color=cclr, linestyle=':',label='prj_'+country2+"(est:"+str(int(result.x[0]))+")")

                            #90% plot
                            d90p = (result.x[1]-parm_90)/result.x[2]
                            plt.plot(d90p, result.x[0]*0.9 , marker='D',color=cclr,fillstyle='none')

                            #p_today = int(ddata[-1]/result.x[0]*100)

                        del ddata[-1]

                    plt.plot(inflex, infley, color=cclr, marker='o',linestyle='--',fillstyle='none')
                   # plt.plot(inflex[0], infley[0], '>')
                    plt.plot(inflex[-1], infley[-1], color=cclr,marker='o',fillstyle='right')
                    plt.plot(inflex[0], infley[0], marker='o',color=cclr)
                    plt.text(inflex[0]+.1, infley[0], country2+'('+str(nsample)+','+str(int(inflex[0]-nsample))+')')
                    #plt.text(inflex[0]+.1, infley[0], country2+'('+str(nsample)+','+str(int(inflex[0]-nsample))+', '+str(p_today)+'%)')

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
pltdata2("Singapore","")
#pltdata2("Turkey","")
#pltdata2("Israel","")
'''
pltdata2("Singapore","")
pltdata2("India","")
pltdata2("Pakistan","")
pltdata2("Malaysia","") 
pltdata2("Philippines","") 
pltdata2("Indonesia","") 
pltdata2("Thailand","") 

pltdata2("Brazil","")
pltdata2("Ecuador","")
pltdata2("Peru","")
'''

'''
day3max = 60-int(np.log10(min_case))*10
day3line = [min_case*2**((i/3)) for i in range(0,day3max)]
plt.plot(range(0,day3max), day3line, label='Dbl every 3d',color='k')
'''
plt.text(30,1500, 'numbers: (sampling size , days to the inflextion point)\nDaimonds: 90% of est. cases\nCurve Eq: f(a,b,c;t)=a/(1+exp(b-ct))\nPython code: https://github.com/Heegon/PyTest')


lastday = str(header[-1].text)
plt.title('Logistic Regression: corona-19 confirmed cases - '+str(min_case)+'th case day to ' +lastday +  '\nand Inflextion point 7-Day Track \ndata: '+url )

plt.yscale('log')
#plt.xscale('log')
#plt.ylim(1000,1000000)
plt.legend(loc='upper left')
plt.show()
