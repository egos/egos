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
from firebase_admin import db, credentials, initialize_app

st.set_page_config(page_title = "egos", layout="wide")



def Fig_conso(dfr,begin, end,idx):
    
    Rolling = [1,2,7,30][idx]
    dfp = dfr[['A','P']].fillna(-1)
    # dfp = dfr.set_index('date')[['A']].fillna(-1) + 1
    dfp = dfp.rolling(Rolling).mean()
    fig = px.line(dfp, color_discrete_map={"A": "blue", "P": "green"})
    # fig = px.area(dfp, color_discrete_map={"A": "blue", "P": "green"}, barmode='group')
    # fig = px.bar(dfp)

    fig.update_layout(        
                    height=500,
                    font=dict(size=16,family = "Arial"),
                    margin=dict(l=10, r=10, t=30, b=10),
                    )
    return fig



if not firebase_admin._apps:
    key = json.loads(st.secrets['textkey'])
    url = "https://my-project-1508716972638-default-rtdb.europe-west1.firebasedatabase.app"
    cred = credentials.Certificate(key)
    app = initialize_app(cred,{'databaseURL' : url} ) 

ref = db.reference("egos/V3")

if 'algo' not in session_state: 
    print(' ')
    print('IMPORT DB')
    algo = {}
    res = ref.get()
    dfr = pd.DataFrame(res).T
    print(dfr.columns)
    # dfr = pd.read_excel("journal_2023.xlsx", engine= "openpyxl",  header=0, sheet_name = "Feuil1", usecols  = "A:AK")
    dfr = dfr[dfr.detail.notnull()]
    dfr.index = pd.to_datetime(dfr.index).date
    # dfr = dfr.set_index('date',drop = False)
    algo = dict(
        dfr= dfr
    )
    algo = SimpleNamespace(**algo)
    session_state['algo'] = algo
else : 
    algo = session_state['algo']

algo = session_state['algo']
dfr  = algo.dfr.copy()
DateToday = datetime.date.today()
with st.expander('Push ', True):
    colActivity = ['sport', 'vel', 'taf', 'Sup', 'projet', 'WB', 'S', 'admin', 'contact','call', 'famille', 'L', 'WTF']
    colConso = ['A', 'P', 'C', 'T','B','Lx','couche']
    colInfo = ['game','Vibe']
    colLocation = ['chup  ','levé', 'matin', 'aprem', 'nuit']
    colTrigger = ['calin','bouffe', 'cauchemar', 'sante', 'vacance']
    colText = ['detail','resum', 'TAF', 'vie']
    ColsLists = [colConso , colActivity , colTrigger ,colInfo ,colLocation]
    ColsTypes = [int,bool,bool, str, str]
    ColsDefaultValue = [0,False, False, '', '']

    stcol  = st.columns(4)
    date  = stcol[0].date_input(
        "Date  / today = " + str(DateToday),
        DateToday,
        format="YYYY-MM-DD",
    )

    Stcol = st.columns(len(ColsLists))
    d = {}
    for i, Cols in enumerate(ColsLists):
        if date in dfr.index: 
            s = dfr.loc[date,Cols]
        else :
            s = pd.Series([ColsDefaultValue[i]] * len(Cols), index = Cols)
        
        s = s.to_frame().T
        # print(s.dtypes)
        # sx = Stcol[i].data_editor(s, hide_index= True)
        sx = st.data_editor(s, hide_index= True)
        d.update(sx.iloc[0].to_dict())
    for c in colText:
        Textdefault = dfr.loc[date,c]  if date in dfr.index else ''
        d[c] = st.text_area(c, Textdefault)

    if (st.button('export')):  ref.update({date.strftime('%Y-%m-%d') : d})


with st.expander('Data', False):
    Stfig = st.container()
    c1, c2 = st .columns([5,1])
    idx = c1.slider('idx',0,3)
    rolling = [1,2,7,30][idx]
    c2.metric("rolling",rolling)


    begin = dfr.index[-12]
    end = dfr.index[-1]

    stcol  = st.columns(4)
    d  = stcol[0].date_input(
        "Select your vacation for next year",
        (begin, end),
        min_value = dfr.index[0],
        max_value = end,
        format="MM-DD-YYYY",
    )
    AllData = stcol[1].toggle('AllData')
    colvrac = ['sport', 'vel', 'taf', 'Sup', 'projet', 'WB', 'S', 'admin', 'contact','call', 'famille', 'L', 'WTF']

    if len(d) ==2 : 
        fig = Fig_conso(dfr,begin, end, idx)
        
        begin , end = d
        mask = (dfr.index >= begin) & (dfr.index <= end)
        # dfr2 = dfr[(dfr.date >= np.datetime64(begin)) & (dfr.date<=np.datetime64(end))]
        dfr2 = dfr[mask]
        if  AllData: 
            fig = Fig_conso(dfr,begin, end, idx)
        else :
            fig = Fig_conso(dfr2 ,begin, end, idx)
        Stfig.plotly_chart(fig, use_container_width=True)

        for idx , row in dfr2.iterrows():
            stcol  = st.columns(3)
            stcol[0].text(idx)
            stcol[1].text(row[['A','P','C']].to_dict())
            data = (row[colvrac].index[row[colvrac].notnull()].tolist())
            stcol[2].text(data)
            # stcol[1].dataframe(row[['A','P','C']])
            st.write(row.detail)
            st.write(row.resum)
            st.write(row.TAF)
            st.divider()
        # st.dataframe(dfr)

