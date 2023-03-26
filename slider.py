import streamlit as st
from datetime import time,timedelta
import pandas as pd
import plotly.express as px 
import json
import datetime
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
col1, col2, col3 = st.columns(3)
col1.metric("ATM", data[str(appointment)]['ATM'], "")
col2.metric("Spot Price", data[str(appointment)]['Spot'], "")
col3.metric("MarketProfile", data[str(appointment)]['Market_Profile_poc'], "")

col1, col2, col3 ,col4= st.columns(4)
col1.metric("CE_COI", pd.DataFrame(data[str(appointment)]['5Strike'])['CE_COI'].apply(int).sum()-pd.DataFrame(data[str(appointment)]['5Strike'])['CE_COI'].apply(int).iloc[0], "")
col3.metric("PE_COI", pd.DataFrame(data[str(appointment)]['5Strike'])['PE_COI'].apply(int).sum()-pd.DataFrame(data[str(appointment)]['5Strike'])['PE_COI'].apply(int).iloc[0], "")

col2.metric("CE_TOI", pd.DataFrame(data[str(appointment)]['5Strike'])['CE_TOI'].apply(int).sum(), "")
col4.metric("PE_TOI", pd.DataFrame(data[str(appointment)]['5Strike'])['PE_TOI'].apply(int).sum(), "")

col1, col2, col3 ,col4= st.columns(4)
col1.metric("CE_COI", pd.DataFrame(data[str(appointment)]['10Strike'])['CE_COI'].apply(int).sum()-pd.DataFrame(data[str(appointment)]['10Strike'])['CE_COI'].apply(int).iloc[0], "")
col3.metric("PE_COI", pd.DataFrame(data[str(appointment)]['10Strike'])['PE_COI'].apply(int).sum()-pd.DataFrame(data[str(appointment)]['10Strike'])['PE_COI'].apply(int).iloc[0], "")

col2.metric("CE_TOI", pd.DataFrame(data[str(appointment)]['10Strike'])['CE_TOI'].apply(int).sum(), "")
col4.metric("PE_TOI", pd.DataFrame(data[str(appointment)]['10Strike'])['PE_TOI'].apply(int).sum(), "")




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
