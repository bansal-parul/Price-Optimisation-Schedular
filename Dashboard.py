# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 02:47:37 2021

@author: pc
"""


import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
import plotly.express as px
from scipy.optimize import minimize
import datetime as dt

def fileUpload(df) -> pd.DataFrame:
    return pd.read_excel(df)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

html_temp = """
<div>
<h1 style ="color:RED;text-align:left;"> Price Recomendation</h1>
"""
st.markdown (html_temp, unsafe_allow_html=True)


df_f=pd.read_csv(r'TSC_sales_forecast_upd.csv')
df_e=pd.read_csv(r'price_eq_upd.csv')
df_a=pd.read_csv(r'TSC_Sales_Data.csv')
df1=pd.read_csv(r'Optimise_Price_2809.csv')
#df1=pd.read_csv(r'C:\Users\pc\Desktop\PriceOptimizationc6dad82\price_rec_2809.csv')
df_price_rec=df1.copy()
df_price_rec[['SCRUB_ITEM','weekday','year']]=df_price_rec['key'].str.split('_',expand=True)

df_a['year']=df_a['TIME_DIM_KEY'].astype(str).str[0:4]
df_a['month']=df_a['TIME_DIM_KEY'].astype(str).str[4:6]
df_a['day']=df_a['TIME_DIM_KEY'].astype(str).str[6:8]
df_a['date']=df_a['year']+'-'+df_a['month']+'-'+df_a['day']
df_a['date']=pd.to_datetime(df_a['date'])
df_a['weekday']=df_a['date'].dt.week


si = st.selectbox("Select one scrub item :", options=df_price_rec['SCRUB_ITEM'].unique().tolist())
st.title('Actual Sales vs Predicted Sales')
df_a['SCRUB_ITEM']=df_a['SCRUB_ITEM'].astype(str)
df_a['TIME_DIM_KEY']=df_a['TIME_DIM_KEY'].astype(str)
df_s_a=df_a[df_a['SCRUB_ITEM'].isin([si])]
df_s_a1=df_s_a.groupby(['weekday','year'])['UNIT_QTY'].sum().reset_index()
df_s_a1['week-year']=df_s_a1['weekday'].astype(str)+'-'+df_s_a1['year'].astype(str)
df_s_a1=df_s_a1.sort_values(['year','weekday'])
df_s_a1['variable']='Actual'
df_f['SCRUB_ITEM']=df_f['SCRUB_ITEM'].astype(str)
df_s_f=df_f[df_f['SCRUB_ITEM'].isin([si])]
df_s_f['week-year']=df_s_f['weekday'].astype(str)+'-'+df_s_f['year'].astype(str)
df_s_f['variable']='Predicted'
df_s_f=df_s_f.sort_values(['year','weekday'])
df_s_f=df_s_f[['week-year','UNIT_QTY','variable']].copy()
df_final=pd.concat([df_s_f,df_s_a1])

fig = px.line(df_final, x="week-year", y="UNIT_QTY", color='variable')

st.plotly_chart(fig)



st.text('Current Price')
df_price=df_a.groupby(['SCRUB_ITEM'])['UNIT_PRICE'].max().reset_index()
df_a_price=df_price[df_price['SCRUB_ITEM']==si]
df_a_price.index=range(0,len(df_a_price))
st.table(df_a_price)
st.text('Recomend price for 1 month')
df=df_price_rec[['SCRUB_ITEM','weekday','year','price']].copy()
df.columns=['SCRUB_ITEM','weekday','year','Recomend_Price']
df_r_price=df[df['SCRUB_ITEM']==si]
df_r_price.index=range(0,len(df_r_price))
st.table(df_r_price)
