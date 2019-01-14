# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 17:54:16 2019
@author: alex1
"""

import pandas as pd
from market_profile import MarketProfile


path = 'D:/export/nf_histrev.txt'
df = pd.read_csv(path)
df.columns = ['symbol','date','time','open','High','Low','Close','volume']
df1 = df.sort_values('time', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
df1 = df.set_index('time', drop=False, append=False, inplace=False, verify_integrity=False)

"split dataframe at new date"
dfsplit = [group[1] for group in df1.groupby(df1.date)]
"get number of splits. Number of splits = Number of days "
nsplits=len(dfsplit) #get number of dataframes = days which is list items
("""Each split dataframe holds intraday data for each day, eg. dfsplit[0] holds o,h,l,c,v intraday data for day1,
 dfsplit[1] holds data for day 2, and so on.""")

"Create empty lists"
date_l=[]
poc_l=[]
vah_l=[]
val_l=[]
xcessh_l=[]
xcessl_l=[]
ibh_l=[]
ibl_l=[]
open_l=[]
high_l=[]
low_l=[]
close_l=[]
vol_l=[]
range_l=[]

"Iterate through each split dataframe so we calculate MP stats for each day and populate empty lists above."
for n in range(0,nsplits):
    
    dfsplit[n]['time'] = pd.to_datetime(dfsplit[n]['time'], format='%H:%M',infer_datetime_format=True).dt.strftime('%H:%M')
    dfsplit[n]['date'] = pd.to_datetime(dfsplit[n]['date'], format='%Y%m%d',infer_datetime_format=True).dt.strftime('%Y%m%d')
    dfsplit[n]['datetime'] = dfsplit[n]['date']+ ' '+dfsplit[n]['time']
    "Set datetime as index and drop datetime column."
    dfsplit[n]=dfsplit[n].set_index('datetime',drop=True)
    dfsplit[n].index = pd.to_datetime(dfsplit[n].index)
    "Remove unwanted columns"
    dfsplit[n]=dfsplit[n].drop(['time','symbol'],axis=1)
    dlow = dfsplit[n]['Low'].min()
    dhigh = dfsplit[n]['High'].max()
    drange=(dhigh-dlow)
    "tick size = 1/35th of daily range. For range of 50 ticksize is 50/35=1.43"
    ticksize=drange/35
    
    mp = MarketProfile(dfsplit[n], tick_size=ticksize,
                       open_range_size=pd.to_timedelta('10 minutes'),
                       initial_balance_delta=pd.to_timedelta('60 minutes'),
                       mode='tpo')
    
    mp_slice = mp[0:len(dfsplit[n].index)]
    data = mp_slice.profile

    df_mp = pd.DataFrame(data)
    df_mp.columns=['TPO']
    df_mp.reset_index(drop=False,inplace=True)
    "Calculate number of TPOs at the lower and higher end of the profile."
    "Lower and higher end is defined as 1/6th of daily range" 
    "Excess at low is true if Excess_low_tpo<15 and close>VAL. It considered as bullish."
    "Run backtest, see if it's valid, have a fun" 
    
    end=drange/6

    excess_low_tpo=df_mp['TPO'].head(int(round(end/ticksize,0))).sum() 
    excess_high_tpo=df_mp['TPO'].tail(int(round(end/ticksize,0))).sum()

    ib=mp_slice.initial_balance()
    ibl=ib[0]
    ibh=ib[1]
    
    date = dfsplit[n].iloc[1]['date']
    date=int(date)

    dopen = dfsplit[n].iloc[0]['open']
    dclose = dfsplit[n].iloc[-1]['Close']

    
    dvolume = dfsplit[n]['volume'].sum()

    val=mp_slice.value_area[0]
    vah=mp_slice.value_area[1]
    poc=mp_slice.poc_price

    date_l.append(date)
    xcessh_l.append(excess_high_tpo)
    xcessl_l.append(excess_low_tpo)
    poc_l.append(poc)
    vah_l.append(vah)
    val_l.append(val)
    ibh_l.append(ibh)
    ibl_l.append(ibl)
    open_l.append(dopen)
    high_l.append(dhigh)
    low_l.append(dlow)
    close_l.append(dclose)
    vol_l.append(dvolume)
    range_l.append(drange)
    
df_mpstats = pd.DataFrame({'date':date_l,'open':open_l,'high':high_l,'low':low_l,'Close':close_l,'volume':vol_l,
                           'VAH':vah_l,'VAL':val_l,'POC':poc_l,'DailyRange':range_l,'ExcessLow':xcessl_l,
                           'ExcessHigh':xcessh_l,'IBhigh':ibh_l,'IBlow':ibl_l})
df_mpstats = df_mpstats.set_index('date',drop=False)

df_mpstats.to_csv('d:/export/mp/mpstats.csv',sep=',',index=False)

"Create custom instrument as 'mymp' and export to csv. Use that custom instrument in prefer s/w for MP stats"
df_mpstats.insert(0, 'symbol', 'mymp')
df_mpstats['date'] = pd.to_datetime(df_mpstats['date'],format='%Y%m%d',infer_datetime_format=False)

df_mpstats[['symbol','date','open','VAH','VAL','POC','DailyRange']].to_csv('d:/export/mp/cust_ticker.csv',sep=',',index=False)
