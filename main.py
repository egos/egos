import streamlit as st
import pandas as pd
import numpy as np
# import networkx as nx
import itertools 
import math
import time
# from math import factorial as f
from datetime import timedelta
from streamlit import session_state
import matplotlib.pyplot as plt
import json
import collections
import copy
# from utils import *
import plotly.express as px
import time
import pickle
from types import SimpleNamespace
import datetime
import firebase_admin
from firebase_admin import firestore

st.set_page_config(page_title = "egos", layout="wide")

def Fig_conso(dfr,begin, end,idx):
    
    Rolling = [1,2,7,30][idx]
    dfp = dfr.set_index('date')[['A','P']].fillna(0)
    dfp = dfp.rolling(Rolling).mean()
    fig = px.line(dfp, color_discrete_map={"A": "blue", "P": "green"})
    fig.update_layout(        
                    height=500,
                    font=dict(size=16,family = "Arial"),
                    margin=dict(l=10, r=10, t=30, b=10),
                    )
    return fig

# key_dict = json.loads(st.secrets['textkey'])
key = json.loads(st.secrets['textkey'])
cred = firebase_admin.credentials.Certificate(key)
url = "https://my-project-1508716972638-default-rtdb.europe-west1.firebasedatabase.app"
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred,    {'databaseURL' : url} ) 

db = firebase_admin.firestore.client()


if 'algo' not in session_state: 
    print(' ')
    print('BEGIN')
    algo = {}
    dfr = pd.read_excel("journal_2023.xlsx", engine= "openpyxl",  header=0, sheet_name = "Feuil1", usecols  = "A:AK")
    dfr = dfr[dfr.detail.notnull()]
    algo = dict(
        dfr= dfr
    )
    algo = SimpleNamespace(**algo)
    session_state['algo'] = algo
else : 
    algo = session_state['algo']

algo = session_state['algo']
dfr  = algo.dfr.copy()

Stfig = st.empty()

c1, c2 = st .columns([5,1])
idx = c1.slider('idx',0,3)
rolling = [1,2,7,30][idx]
c2.metric("rolling",rolling)
# c2.write([1,2,7,30][idx])
# print(idx, [1,2,7,30][idx])
begin = dfr.iloc[len(dfr)-12].date
end = dfr.iloc[-1].date

stcol  = st.columns(4)
d  = stcol[0].date_input(
    "Select your vacation for next year",
    (begin, end),
    min_value = dfr.iloc[0].date,
    max_value = end,
    format="MM-DD-YYYY",
)
AllData = stcol[1].toggle('AllData')
colvrac = ['sport', 'vel', 'taf', 'Sup', 'projet', 'WB', 'S', 'admin', 'contact','call', 'famille', 'L', 'WTF']

if len(d) ==2 : 
    fig = Fig_conso(dfr,begin, end, idx)
    
    begin , end = d
    
    dfr2 = dfr[(dfr.date >= np.datetime64(begin)) & (dfr.date<=np.datetime64(end))]
    if  AllData: 
        fig = Fig_conso(dfr,begin, end, idx)
    else :
        fig = Fig_conso(dfr2 ,begin, end, idx)
    Stfig.plotly_chart(fig, use_container_width=True)

    for idx , row in dfr2.iterrows():
        stcol  = st.columns(3)
        stcol[0].text(row.date.strftime("%A-%d-%B-%Y"))
        stcol[1].text(row[['A','P','C']].to_dict())
        data = (row[colvrac].index[row[colvrac].notnull()].tolist())
        stcol[2].text(data)
        # stcol[1].dataframe(row[['A','P','C']])
        st.write(row.detail)
        st.write(row.resum)
        st.write(row.TAF)
        st.divider()
    # st.dataframe(dfr)

