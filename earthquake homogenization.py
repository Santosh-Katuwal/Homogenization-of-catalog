'''
Magnitude conversion tool
Source:
Empirical conversion between teleseismic magnitudes (mb andMs)
and moment magnitude (Mw) at the Global, Euro-Mediterranean
and Italian scale (doi: 10.1093/gji/ggu264)
Geophys. J. Int. (2014) 199, 805–828


1) Surface wave magnitude to moment magnitude conversion
Mw = exp(2.133 + 0.063Ms) − 6.205, Ms ≤ 5.5
Mw = exp(−0.109 + 0.229Ms) + 2.586, Ms > 5.5

2)body wave magnitude moment magnitude conversion
Mw = exp (0.741 + 0.210mb) − 0.785

3) Local Magnitude to moment magnitude conversion
    Mw=2*Ml/3 + 1.15
    
    Source:
        Munafò, I., Malagnini, L., & Chiaraluce, L. (2016). On the Relationship betweenMw and ML
        for Small Earthquakes. Bulletin of the Seismological Society of America, 106(5), 
        2402–2408. doi:10.1785/0120160130 

#Types of Magnitudes as per USGS:
https://www.usgs.gov/natural-hazards/earthquake-hazards/science/magnitude-types?qt-science_center_objects=0#qt-science_center_objects


'''

import pandas as pd
import numpy as np
import os
from PyQt5 import QtWidgets
import sys
import win32ui
import math
import datetime as dt


#Reading Raw Catalog
cwd=os.getcwd()
cat=pd.read_csv(cwd+'\\input_catalog.csv')

YYYY=[]
MM=[]
DD=[]
lat=[]
lon=[]
dep=[]
mag=[]
un=[]
n=len(cat)

for i in range(0,n):
    YYYY_i=cat.iloc[i,0]
    MM_i=cat.iloc[i,1]
    DD_i=cat.iloc[i,2]
    lat_i=cat.iloc[i,3]
    lon_i=cat.iloc[i,4]
    dep_i=cat.iloc[i,5]
    mag_i=cat.iloc[i,6]
    un_i=cat.iloc[i,7]
    
    YYYY.append(YYYY_i)
    MM.append(MM_i)
    DD.append(DD_i)
    lat.append(lat_i)
    lon.append(lon_i)
    dep.append(dep_i)
    mag.append(mag_i)
    un.append(un_i)

    i=i+1

con_mag=[]
form=[]
for i in range(0,n):
    
    if un[i]=='mw' or un[i]=='mww' or un[i]=='mwc' or un[i]=='mwr' or un[i]=='mwb':
        con_mag_i=mag[i]
        
    elif un[i]=='mb':
        con_mag_i=round(np.exp(0.741+0.210*mag[i])-0.785,1)
                
    elif un[i]=='ms' and mag[i]<=5.5:
        con_mag_i=round(np.exp(2.133+0.063*mag[i])-6.205,1)
                
    elif un[i]=='ms' and mag[i]>5.5:
        con_mag_i=round(np.exp(-0.109+0.229*mag[i])+2.586,1)
        
        
    elif un[i]=='ml':
        con_mag_i=round((2*mag[i]/3)+1.15,1)
                
    else:
        con_mag_i=mag[i]
    
    con_mag.append(con_mag_i)
    

    i=i+1

unit=[]
for i in range (0,n):
    unit_i='mw'
    unit.append(unit_i)
    
    i=i+1

date=[]
for i in range(0,n):
    date_i=dt.date(YYYY[i],MM[i],DD[i])
    date.append(date_i)
combined=pd.DataFrame({'date':date,
                       'latitude':lat,
                       'longitude':lon,
                       'depth':dep,
                       'mag':con_mag,
                       'magType':unit})
combined=combined.sort_values(by='date',ascending=True)
combined=combined.reset_index()
combined=combined.drop(columns='index')
yyyy=[]
mm=[]
dd=[]
for i in range(0,n):
    yyyy_i=combined.date[i].year
    mm_i=combined.date[i].month
    dd_i=combined.date[i].day
    
    yyyy.append(yyyy_i)
    mm.append(mm_i)
    dd.append(dd_i)
    
out=pd.DataFrame({'yyyy':yyyy,
                  'mm':mm,
                  'dd':dd,
                  'latitude':combined.latitude,
                  'longitude':combined.longitude,
                  'depth': combined.depth,
                  'mag':combined.mag,
                  'magType':combined.magType})
 
OUT=out   
OUT.to_csv(cwd+'\\out_homogenized.csv', index = False)
    

    
    