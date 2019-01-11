
import pandas as pd
import matplotlib.pyplot as plt
from market_profile import MarketProfile

"read data from csv or comma delimited text file, change the path accordingly"
#path = 'C:/Users/alex1/Dropbox/Python2/nf_hist.txt'
path = 'd:/export/_NF1.txt'
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

"You can change the mode to volume by replacing mode='tpo' with 'vol'. Keep tick size for Nifty as 1 and for Emini 0.25" 
#mp = MarketProfile(df, tick_size=5, mode='tpo')
mp = MarketProfile(df, tick_size=5,
                   open_range_size=pd.to_timedelta('10 minutes'),
                   initial_balance_delta=pd.to_timedelta('60 minutes'),
                   mode='tpo')

"If you have more than 1 days of intra data then use following line. Note for the US market replace 6.20 by 6.50" 
#mp_slice = mp[df.index.max() - pd.Timedelta(6.20, 'h'):df.index.max()]
"If you have only current days data then use following line"
mp_slice = mp[0:len(df.index)]

data = mp_slice.profile
data.plot(kind='barh')

print( "Initial balance: %f, %f" % mp_slice.initial_balance())
print( "Opening range: %f, %f" % mp_slice.open_range())
print( "POC: %f" % mp_slice.poc_price)
print( "Profile range: %f, %f" % mp_slice.profile_range)
print( "Value area: %f, %f" % mp_slice.value_area)
print( "Balanced Target: %f" % mp_slice.balanced_target)
val=mp_slice.value_area[0]
vah=mp_slice.value_area[1]
poc=mp_slice.poc_price
"PLot value area as horizontal lines on price chart and save the plot as image in local disk"
plt.figure()
plt.axhline(y=vah,linewidth=2, color='green')
plt.axhline(y=val,linewidth=2, color='red')
plt.axhline(y=poc,linewidth=2, color='yellow')
fig = plt.gcf()
fig.set_size_inches(22, 10.5)
"Change the folder name"
fig.savefig('d:/export/mymp.png', dpi=98, bbox_inches='tight', pad_inches=0.1)
#plt.plot(df.close)
view rawnfmp.py hosted with ❤ by GitHub
