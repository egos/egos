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

st.set_page_config(page_title = "egos", layout="wide")

file = "journal_2023.xlsx"
dfr = pd.read_excel(file, engine= "openpyxl",  header=0, sheet_name = "Feuil1", usecols  = "A:AK")
dfr = dfr[dfr.detail.notnull()]
# dfr.loc[dfr==None] = np.NAN
fig = px.line(dfr.set_index('date')[['A','P']].rolling(7).mean(), color_discrete_map={"A": "blue", "P": "green"})
fig.update_layout(        
                # yaxis_title ='count',
                # xaxis_title ='epoch',
                height=500,
                font=dict(size=16,family = "Arial"),
                margin=dict(l=10, r=10, t=30, b=10),
                )


st.plotly_chart(fig, use_container_width=True)
# datetime.date(2019, 7, 6)
begin = dfr.iloc[len(dfr)-12].date
end = dfr.iloc[-1].date
stcol  = st.columns(4)
# begin  = stcol[0].date_input("begin", begin)
# end  = stcol[1].date_input("end", end)


d  = stcol[0].date_input(
    "Select your vacation for next year",
    (begin, end),
    max_value  = end,
    format="MM-DD-YYYY",
)

colvrac = ['sport', 'vel', 'taf', 'Sup', 'projet', 'WB', 'S', 'admin', 'contact',
       'call', 'famille', 'L', 'WTF']
if len(d) ==2 : 
    begin , end = d
    dfr = dfr[(dfr.date >= np.datetime64(begin)) & (dfr.date<=np.datetime64(end))]
    for idx , row in dfr.iterrows():
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

