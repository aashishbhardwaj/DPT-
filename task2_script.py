# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 18:14:14 2018

@author: bhard_ab
"""
import os
import pandas
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import csv
import pandas as pd


def getdatetime(x):
    return datetime.strptime(x[0]+','+x[1], '%d-%m-%Y,%H:%M:%S')

d=[ "06:46:19" ,"07:09:43" ,"07:34:04" ,"08:17:44" ,"8:24:09" ,"08:25:48" ,"08:53:33" ,"09:25:08" ,"09:36:13" ,"09:50:13" ,
                           "09:59:03" ,"10:27:53" ,"10:39:28" ,"10:52:28" ,"11:03:22" ,"11:41:07" ,"11:52:22" ,"12:05:57" ,"12:15:17" ,
                           "12:48:47" ,"12:54:37" ,"13:16:57" ,"13:26:17" ,"13:58:06" ,"14:03:36" ,"14:25:06" ,"14:34:26" ,"15:01:41" ,"15:07:16" ,
                           "15:29:36" ,"15:36:31" ,"16:05:15" ,"16:08:40" ,"16:35:30" ,"16:41:00" ,"17:11:45" ,"17:14:35" ,"17:36:00" ,"17:44:55" ,
                           "18:18:25" ,"18:23:15" ,"18:44:59" ,"18:55:54", "19:25:34"]



n=len(d)
a=list(range(0, n, 4))
b=list(range(1, n, 4))
c=sorted(a+b)


d_suc = list( d[i] for i in c)
df=pd.DataFrame({'Tijd':d_suc })

df["date"]="11-Jul-2018"

df["Time"]=df["date"] + " " + df["Tijd"]
df.Time=pd.to_datetime(df.Time)

################
#original Data
################
df2=pd.read_csv("D:/02_Projects/06_Python/03_ebi/Acquisition_EVENT_20180711_11.log")

df2.columns=['Datum','Tijd','x','y','z','Dichtheid','Leidingsnelheid','Waterverplaasting','Volume','TDS']
Time= df2[['Datum','Tijd']].apply(getdatetime, axis=1)
df2["Time"]=Time

col = ['Time', 'x', 'y','z']
df2=df2[col]   
   
################
#loop
################
df3=pd.DataFrame()
r=len(df)

klm=np.arange(0,r,2)

for i in klm:
        mn=df2[(df2['Time'] >= df.iloc[i,2]) & (df2['Time'] <= df.iloc[i+1,2])]
        df3 = df3.append(mn)
           
df3.to_csv("d9_suction.csv", index=False)













