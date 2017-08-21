# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 18:33:49 2017

@author: bhard_ab
"""

import os
import glob
import pandas as pd
import numpy as np


os.chdir("C:/06_hongkong/HKO")
df1=pd.read_csv( "rf_HKO_hourly.txt" ,sep=' ', skipinitialspace=True ,header= 0, skiprows=2, parse_dates=["Date"],  infer_datetime_format=True )
df1['Date'] = df1['Date'] + pd.to_timedelta(df1['hour'], unit="h")
df1.index= df1.Date
df1=df1.drop("Date",1)
df1=df1.drop("hour",1)


df2=pd.read_csv( "dew_HKO.txt",sep=' ', skipinitialspace=True ,header= 0, skiprows=1, parse_dates=["Date"],  infer_datetime_format=True )
df2['Date'] = df2['Date'] + pd.to_timedelta(df2['hour'], unit="h")
df2.index= df2.Date
df2=df2.drop("point(degree",1)
df2=df2.drop("Celsius)",1)
df2=df2.drop("hour",1)
df2=df2.drop("Date",1)


df3= df2.join(df1,how='left')

df3.columns = (["DPT","PPT"])

df3.loc[df3['PPT'] == 'Trace', 'PPT' ] = 0.04

#df3.to_csv("obs_HKO.csv")

df3.DPT = df3.DPT.shift(-4)
df4=df3.dropna()


df5=pd.DataFrame((df4.loc['1981-01-01 00:00:00':'2010-12-31 23:00:00'])) 
df5.PPT= df5.PPT.astype(float)
df6 = df5[df5.PPT != 0]

##########################################################################
def rl2(dg,qv,cc,scc):
  

  mn=np.round(min(dg.DPT)-2)
  mx=np.round(max(dg.DPT)+2)
  mv= 100/(100-(100*qv))
  dg['bin']=pd.cut(dg['DPT'],range(int(mn),int(mx)))
  j=dg[dg.groupby('bin').PPT.transform(len) > mv] # here we check number of variables
  hm=j.groupby(by=["bin"],as_index=True)
  qt= hm.quantile(q=qv,numeric_only= False)
  qt=qt[(qt >= 0).all(1)] # allow only to take positive values including zeero
  qt["ma"]= qt.PPT.rolling(window=3,center=True).mean()
  qt["ma"]=qt.ma.fillna(method='bfill')
  qt["ma"]=qt.ma.fillna(method='ffill')

  qt['cc']=0
  qt['scc']=0
  nr=qt.shape[0]
  ini=qt.iloc[0,1]
  qt.iloc[0,3]=ini
  qt.iloc[0,4]=ini
  for i in range(1,nr):
      qt.iloc[i,3]=qt.iloc[i-1,3] + qt.iloc[i-1,3]* (float(cc)/100)
      qt.iloc[i,4]=qt.iloc[i-1,4] + qt.iloc[i-1,4]* (float(scc)/100)   
      
  qt['slp']=0
  qt['per']=0      
  n=0
   
  for i in range(1,nr):
      
      if((n+1) < qt.shape[0]):
          qt.iloc[n+1,5]= ((qt.iloc[n+1,2]-qt.iloc[n,2])/(qt.iloc[n+1,0]-qt.iloc[n,0]))
          if((n+2) < qt.shape[0]):
              qt.iloc[n+2,6]=(((qt.iloc[n+2,2]-qt.iloc[n+1,2])/(qt.iloc[n+2,0]-qt.iloc[n+1,0]))-((qt.iloc[n+1,2]-qt.iloc[n,2])/(qt.iloc[n+1,0]-qt.iloc[n,0]))) #relative slope increase
#              qt.iloc[n,6]=(((qt.iloc[n+2,2]-qt.iloc[n+1,2])/(qt.iloc[n+2,0]-qt.iloc[n+1,0]))-((qt.iloc[n+1,2]-qt.iloc[n,2])/(qt.iloc[n+1,0]-qt.iloc[n,0])))*(100/((qt.iloc[n+1,2]-qt.iloc[n,2])/(qt.iloc[n+1,0]-qt.iloc[n,0])))
              pass
      else:
          pass
      n=n+1    
#  qt['mv']= pd.rolling_mean(qt.slp,3, center=True)
#  qt.plot(x="DPT",y=["Precipitation","Prm"], grid=True, yticks= (1,2,3,4,5), kind= "line")
  Title="Relationship with "+str(qv*100)+" percentile"   
  pg=str(qv)+"_quantile.jpg"      
#  qt.plot(x=qt.DPT,y=["PPT","cc", "scc"], grid=True, logy=True, kind= "line", style=['-','g--','r--'])
  cv=qt.plot(x=qt.DPT,y=["PPT","cc", "scc"],grid=True, logy=True, kind= "line", style=['-','g--','r--'],title=Title, ylim = [0,100],  yticks=np.arange(-10,101,10)) 
#  cv=qt.plot(x="DPT",y=["Precipitation","Prm"], grid=True, yticks= (5,10,15,20,25,30), kind= "line")
  g=cv.get_figure() #this get the IDF figure
  g.savefig(pg)
  return qt
  
##########################
we=rl2(df6,0.999,7,14)   
we=rl2(df6,0.99,7,14)
we=rl2(df6,0.95,7,14)
we=rl2(df6,0.90,7,14)
we=rl2(df6,0.80,7,14)
we=rl2(df6,0.70,7,14)


#######################################
cs=list((0.999,0.99,0.9,0.70))
for i in cs:
    we=rl2(df6,i,7,14)
