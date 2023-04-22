import streamlit as st
from datetime import time,timedelta
import pandas as pd
import plotly.express as px 
import json
import math
import datetime
import numpy as np
from numpy import nan
import os
st.set_page_config(layout="wide")
dates=[]
filesnames=[]
for i in os.listdir():
    if '.json' in i:
        if os.stat(i).st_size >100:
            print(i)
            filesnames.append(i)
            dates.append(i.replace('BANKNIFTY_','').replace('_at_minute.json',''))
o=st.selectbox('Select Date :',dates)
st.write('Display Date is:', o)
# Opening JSON file
m=st.sidebar.text_input('Option Range',value=10)


for i in filesnames:
    if o in i:
        with open('{}'.format(i)) as json_file:
            data = eval(json.load(json_file))
         
            # Print the type of data variable
            print("Type:", type(data))
appointment = st.slider(    "Select Market time:",    min_value=time(9, 15),max_value=time(15,30),    value=time(9, 16),step=timedelta(minutes=1))
st.write("Current Market Time:", appointment)

col1, col2, col3 ,col4= st.columns(4)
col1.metric("ATM", data[str(appointment)]['ATM'], "")
col2.metric("Spot Price", data[str(appointment)]['Spot'], "")
col3.metric("MarketProfile", data[str(appointment)]['Market_Profile_poc'], "")
col4.metric("VolumeProfile", data[str(appointment)]['Volume_Profile_poc'], "")

data1=data[str(appointment)]

eodselect=pd.DataFrame.from_dict(data1['10Strike'])
strikes=[]
for i in range(0,6):
    strikes.append(data1['ATM']+(i*100))
    strikes.append(data1['ATM']-(i*100))
eodselect=eodselect[eodselect['#'].isin(strikes)]
eodselect['PCR']=round((eodselect['PE_TOI']/eodselect['CE_TOI']),2)
eodselect['CPR']=round((eodselect['CE_TOI']/eodselect['PE_TOI']),2)
eodselect['CE_PCT']=round((eodselect['CE_PCT']),2)
eodselect['PE_PCT']=round((eodselect['PE_PCT']),2)
eodselect['CE_PCT']=eodselect['CE_PCT'].apply(str)+'%'
eodselect['PE_PCT']=eodselect['PE_PCT'].apply(str)+'%'


df=(eodselect[['#','CE_TOI','PE_TOI','CPR','PCR','CE_COI','PE_COI','CE_INOI','PE_INOI','CE_PCT','PE_PCT']].iloc[::-1])
R=[]
S=[]
for i in range(0,6):
    if not (df[(df['CPR']>= 1.5) & (df['#']==(data1['ATM']+(i*100)))]).empty:
        print(str(data1['ATM']+(i*100)))
        R.append(data1['ATM']+(i*100))
    if not (df[(df['PCR']>= 1.5) & (df['#']==(data1['ATM']-(i*100)))]).empty:
        print(str(data1['ATM']-(i*100)))
        S.append(data1['ATM']-(i*100))
        
R=[]
S=[]
for i in range(0,6):
    if not (df[(df['CPR']>= 1.5) & (df['#']==(data1['ATM']+(i*100)))]).empty:
        print(str(data1['ATM']+(i*100)))
        R.append(data1['ATM']+(i*100))
    if not (df[(df['PCR']>= 1.5) & (df['#']==(data1['ATM']-(i*100)))]).empty:
        print(str(data1['ATM']-(i*100)))
        S.append(data1['ATM']-(i*100))
        
R=R[:3]
S=S[:3]
df1=pd.DataFrame([R,S],columns=['R/S_1','R/S_2','R/S_3'])  
df1.index=['R','S']
st.dataframe(df1)
st.dataframe(pd.DataFrame.from_dict(data1['poc_df']))
poc_i=pd.DataFrame(data1['poc_concl'][:data1['poc_n']],columns=['time','Strike','CE_COI','PE_COI','Diff','CE_PCT','PE_PCT']).iloc[::-1]
poc_i['PCT_Diff']=poc_i['PE_PCT']-poc_i['CE_PCT']
st.dataframe(poc_i)
vp=data[str(appointment)]['VolumeProfile']
mp=data[str(appointment)]['MarketProfile']
df2=pd.DataFrame([[int(vp['poc']),int(vp['low']),int(vp['high']),int(vp['val']),int(vp['vah']),int(vp['or_low']),int(vp['or_high']),int(vp['ib_low']),int(vp['ib_high']),int(vp['bt'])],
[int(mp['poc']),int(mp['low']),int(mp['high']),int(mp['val']),int(mp['vah']),int(mp['or_low']),int(mp['or_high']),int(mp['ib_low']),int(mp['ib_high']),int(mp['bt'])]],columns=['POC','Low','High','VAL','VAH','Or_low','Or_High','IB_Low','IB_High','BT'])
df2.index=['VolumeProfile','MarketProfile']
st.dataframe(df2)

CE_COI_5=pd.DataFrame(data[str(appointment)]['5Strike'])['CE_COI'].apply(int).sum()
PE_COI_5=pd.DataFrame(data[str(appointment)]['5Strike'])['PE_COI'].apply(int).sum()
CE_COI_10=pd.DataFrame(data[str(appointment)]['10Strike'])['CE_COI'].apply(int).sum()
PE_COI_10=pd.DataFrame(data[str(appointment)]['10Strike'])['PE_COI'].apply(int).sum()

CE_TOI_5=pd.DataFrame(data[str(appointment)]['5Strike'])['CE_TOI'].apply(int).sum()
PE_TOI_5=pd.DataFrame(data[str(appointment)]['5Strike'])['PE_TOI'].apply(int).sum()
CE_TOI_10=pd.DataFrame(data[str(appointment)]['10Strike'])['CE_TOI'].apply(int).sum()
PE_TOI_10=pd.DataFrame(data[str(appointment)]['10Strike'])['PE_TOI'].apply(int).sum()

df3=pd.DataFrame([[CE_COI_5,PE_COI_5,CE_TOI_5,PE_TOI_5],[CE_COI_10,PE_COI_10,CE_TOI_10,PE_TOI_10]],
             columns=['CE_COI','PE_COI','CE_TOI','PE_TOI'])
df3.index=['5_Strike','10_Strike']
df3['COI_Diff']=df3['PE_COI']-df3['CE_COI']
df3['COI_Decision']=np.where((df3['PE_COI']/df3['CE_COI']) >1.5,'BUY' ,np.where((df3['PE_COI']/df3['CE_COI'])>1,'Strong Buy',np.where((df3['PE_COI']/df3['CE_COI'])<0.5,'Strong SELL','Sell')))
df3['TOI_Decision']=np.where((df3['PE_TOI']/df3['CE_TOI']) >1.5,'BUY' ,np.where((df3['PE_TOI']/df3['CE_TOI'])>1,'Strong Buy',np.where((df3['PE_TOI']/df3['CE_TOI'])<0.5,'Strong SELL','Sell')))
df3['TOI_Diff']=df3['PE_TOI']-df3['CE_TOI']
#df3['COI_Position']=df3['PE_']
df3=df3[['CE_COI','PE_COI','COI_Diff','COI_Decision','CE_TOI','PE_TOI','TOI_Diff','TOI_Decision']]
st.dataframe(df3)
#st.write(data)
#st.write(data[str(appointment)])
st.dataframe(df)
st.write(data1['poc_n'])
st.write('Volume Profile')
st.json(vp)
st.write('Market Profile')
st.json(mp)

st.write('EOD')

k=pd.DataFrame.from_dict(data['EOD'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig=px.bar(k, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE_TOI':'#FF2B2B','CE_COI':'#FFABAB','PE_TOI':'#0068C9','PE_COI':'#83C9FF'})
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.plotly_chart(fig,  theme="streamlit",use_container_width=True)



k=pd.DataFrame.from_dict(data[str(appointment)]['5Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig=px.bar(k, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE_TOI':'#FF2B2B','CE_COI':'#FFABAB','PE_TOI':'#0068C9','PE_COI':'#83C9FF'})
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.plotly_chart(fig,  theme="streamlit",use_container_width=True)
#st.write(fig)
k=pd.DataFrame.from_dict(data[str(appointment)]['10Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig=px.bar(k, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE_TOI':'#FF2B2B','CE_COI':'#FFABAB','PE_TOI':'#0068C9','PE_COI':'#83C9FF'})
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
#st.write(fig)
st.plotly_chart(fig,  theme="streamlit",use_container_width=True)


import plotly.graph_objects as go
fig = go.Figure()
k=pd.DataFrame.from_dict(data[str(appointment)]['5Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig.add_trace(go.Bar(name='CE %', x=k.index, y=k.CE_COI ,offsetgroup=0,base=k.CE_TOI,marker_color = '#83C9FF'))
fig.add_trace(go.Bar(name='CE', x=k.index, y=k.CE_TOI ,offsetgroup=0,marker_color='#0068C9'))

fig.add_trace(go.Bar(name='PE', x=k.index, y=k.PE_TOI,offsetgroup=1,marker_color='#FF2B2B'))
fig.add_trace(go.Bar(name='PE %', x=k.index, y=k.PE_COI,offsetgroup=1,base=k.PE_TOI,marker_color='#FFABAB'))
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.plotly_chart(fig,  theme="streamlit",use_container_width=True)
fig = go.Figure()

k=pd.DataFrame.from_dict(data[str(appointment)]['10Strike'])

k.index=k['#']#.apply(int)

k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]

fig.add_trace(go.Bar(name='CE %', x=k.index, y=k.CE_COI ,offsetgroup=0,base=k.CE_TOI,marker_color = '#83C9FF'))
fig.add_trace(go.Bar(name='CE', x=k.index, y=k.CE_TOI ,offsetgroup=0,marker_color='#0068C9'))

fig.add_trace(go.Bar(name='PE', x=k.index, y=k.PE_TOI,offsetgroup=1,marker_color='#FF2B2B'))
fig.add_trace(go.Bar(name='PE %', x=k.index, y=k.PE_COI,offsetgroup=1,base=k.PE_TOI,marker_color='#FFABAB'))

st.plotly_chart(fig,  theme="streamlit",use_container_width=True)



st.dataframe(pd.DataFrame.from_dict(data[str(appointment)]['5Strike']))

st.dataframe(pd.DataFrame.from_dict(data[str(appointment)]['10Strike']))
