import streamlit as st
from datetime import time,timedelta
import pandas as pd
import plotly.express as px 
import json
import datetime
import os
dates=[]
filesnames=[]
for i in os.listdir():
    if '.json' in i:
        if os.stat(i).st_size >100:
            print(i)
            filesnames.append(i)
            dates.append(i.replace('BANKNIFTY_','').replace('_at_minute.json',''))
o=st.selectbox('Select Date :',dates)
st.write('Display Date is:', datetime.date(2023, 3, 9))
# Opening JSON file

for i in filesnames:
    if o in i:
        
        with open('{}'.format(i)) as json_file:
            data = json.load(json_file)
         
            # Print the type of data variable
            print("Type:", type(data))
appointment = st.slider(    "Select Market time:",    min_value=time(9, 15),max_value=time(15,30),    value=time(9, 16),step=timedelta(minutes=1))
st.write("Current Market Time:", appointment)


#st.write(data[str(appointment)])

st.write('ATM {}'.format(data[str(appointment)]['ATM']))

st.write('Spot Price {}'.format(data[str(appointment)]['Spot']))

st.write('MarketProfile POC {}'.format(data[str(appointment)]['Market_Profile_poc']))

k=pd.DataFrame.from_dict(data[str(appointment)]['5Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig=px.bar(k, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE_TOI':'#FF2B2B','CE_COI':'#FFABAB','PE_TOI':'#0068C9','PE_COI':'#83C9FF'})
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.write(fig)
k=pd.DataFrame.from_dict(data[str(appointment)]['10Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig=px.bar(k, orientation='h' ,text_auto=True,barmode='group',color_discrete_map={'CE_TOI':'#FF2B2B','CE_COI':'#FFABAB','PE_TOI':'#0068C9','PE_COI':'#83C9FF'})
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.write(fig)


import plotly.graph_objects as go
fig = go.Figure()
k=pd.DataFrame.from_dict(data[str(appointment)]['5Strike'])
k.index=k['#']#.apply(int)
k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]
fig.add_trace(go.Bar(name='CE %', x=k.index, y=k.CE_COI ,offsetgroup=0,base=k.PE_TOI,marker_color = '#83C9FF'))
fig.add_trace(go.Bar(name='CE', x=k.index, y=k.CE_TOI ,offsetgroup=0,marker_color='#0068C9'))

fig.add_trace(go.Bar(name='PE', x=k.index, y=k.PE_TOI,offsetgroup=1,marker_color='#FF2B2B'))
fig.add_trace(go.Bar(name='PE %', x=k.index, y=k.PE_COI,offsetgroup=1,base=k.PE_TOI,marker_color='#FFABAB'))
fig.update_traces(textfont_size=27, textangle=0, textposition="outside", cliponaxis=False)
st.write(fig)

fig = go.Figure()

k=pd.DataFrame.from_dict(data[str(appointment)]['10Strike'])

k.index=k['#']#.apply(int)

k=k[['CE_COI',   'CE_TOI'  ,'PE_COI',  'PE_TOI']]

fig.add_trace(go.Bar(name='CE %', x=k.index, y=k.CE_COI ,offsetgroup=0,base=k.CE_TOI,marker_color = '#83C9FF'))
fig.add_trace(go.Bar(name='CE', x=k.index, y=k.CE_TOI ,offsetgroup=0,marker_color='#0068C9'))

fig.add_trace(go.Bar(name='PE', x=k.index, y=k.PE_TOI,offsetgroup=1,marker_color='#FF2B2B'))
fig.add_trace(go.Bar(name='PE %', x=k.index, y=k.PE_COI,offsetgroup=1,base=k.PE_TOI,marker_color='#FFABAB'))

st.write(fig)


st.dataframe(pd.DataFrame.from_dict(data[str(appointment)]['5Strike']))

st.dataframe(pd.DataFrame.from_dict(data[str(appointment)]['10Strike']))
