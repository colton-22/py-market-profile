# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 17:36:51 2019

@author: alex1
"""

import pandas as pd
import matplotlib.pyplot as plt
from market_profile import MarketProfile
import numpy as np
from detect_peaks import detect_peaks

("""Detect peaks and valleys taken from 
 https://nbviewer.jupyter.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb""")

#def mpstats(ticksize=2,mymode='tpo'):
def xcesslvn(mymode='vol'):
    
    
    "read data from csv or comma delimited text file, change the path accordingly"
    #path = 'C:/Users/alex1/Dropbox/Python2/nf_hist.txt'
    path = 'd:/export/_NIFTY_xcess.txt'
    df = pd.read_csv(path, sep=",")
    "No headers in the csv so let's assign them. If data format is diferent then chnage accordingly but column name 'Close' has to be in capital"
    df.columns = ['symbol','date','time','Open','High','Low','Close','Volume']
    
    ("""Convert date and time to pandas datetime format. First merge date and time column, if your data is already in datetime 
     format then skip foloowing 3 lines""")
    df['time'] = pd.to_datetime(df['time'], format='%H:%M',infer_datetime_format=True).dt.strftime('%H:%M')
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d',infer_datetime_format=True).dt.strftime('%Y%m%d')
    df['datetime'] = df['date']+ ' '+df['time']
    "Set datetime as index and drop datetime column."
    df=df.set_index('datetime',drop=True)
    df.index = pd.to_datetime(df.index)
    "Remove unwanted columns"
    df=df.drop(['date','time','symbol'],axis=1)
    
    dlow = df['Low'].min()
    dhigh = df['High'].max()
    drange=(dhigh-dlow)
    "tick size = 1/25th of daily range. For range of 50 ticksize is 50/25=2"
    ticksize=drange/35
    
    mp = MarketProfile(df, tick_size=ticksize,
                       open_range_size=pd.to_timedelta('10 minutes'),
                       initial_balance_delta=pd.to_timedelta('60 minutes'),
                       mode=mymode)
    
    "If you have more than 1 days of intra data then use following line. Note for the US market replace 6.20 by 6.50" 
    #mp_slice = mp[df.index.max() - pd.Timedelta(6.20, 'h'):df.index.max()]
    "If you have only current days data then use following line"
    mp_slice = mp[0:len(df.index)]
    
    data = mp_slice.profile
    #data.plot(kind='barh')
    
    "DataFrame df_mp to calculate excess and LVNs"
    df_mp = pd.DataFrame(data)
    df_mp.columns=['TPO']
    df_mp.reset_index(drop=False,inplace=True)
    
    "Calculate Number of TPOs at lower and higher end of the profile."
    "Lower and higher end is defined as 1/6th of daily range"     
    end=drange/6
    
    excess_low_tpo=df_mp['TPO'].head(int(round(end/ticksize,0))).sum() 
    excess_high_tpo=df_mp['TPO'].tail(int(round(end/ticksize,0))).sum()
    
    x=df_mp['TPO'].values
    ind=detect_peaks(x, mph=df_mp['TPO'].max(), mpd=10, valley=True, show=False)
    lvn_list=[]
    "Convert numpy array to list"
    indl=np.ndarray.tolist(ind)
    
    for i in indl:
        print(i)
        lvn_l=df_mp.iloc[i]['Close']
        lvn_list.append(lvn_l)
    return(excess_low_tpo, excess_high_tpo,lvn_list)

"How to use example"
from def_xcesslvn import xcesslvn
gt=xcesslvn(mymode='tpo')
xcess_low = gt[0]
xcess_high=gt[1]

gv=xcesslvn(mymode='vol')
lvn_list=gv[2]
print('TPOs near low: ',xcess_low,', TPOs near high: ',xcess_high,', LVNs: ',lvn_list)
