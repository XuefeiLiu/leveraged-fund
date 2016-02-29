# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:38:35 2016

@author: Hansen Wang
"""
import pandas as pd
from KJmodel1223_2 import B
from formatdivert import formatdivertBM, formatdivertA
import os

fn = os.path.join(os.path.dirname(__file__), 'data')
df_A_nav=pd.read_csv(fn+'/NAVA.csv')
df_A_nav=formatdivertA(df_A_nav)
#print(df_A_nav.columns)
date_ls = df_A_nav['date'].tolist()
#print(date_ls)
date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])
#print(date_ls)

cash=1000000
account=0

startdate="01/04/2016"
enddate="20160205"

K = 3
J = 3

KJ=B(cash,account,startdate,K,J)
KJ_moneyrecord=KJ.test(startdate,K,J,cash,1,enddate)
print(KJ_moneyrecord)
benchmark_moneyrecord=KJ.benchtest(startdate,cash,enddate)


KJ.plot_contrast(KJ_moneyrecord,benchmark_moneyrecord,date_ls,startdate,enddate)
alpha=pd.DataFrame()
date_ls_change=[]
start=KJ.datetransfer(startdate)
for i in date_ls:
    if int(i)>=int(start) and int(i)<=int(enddate):
        date_ls_change.append(i)
for i in date_ls_change:
    alpha_i=KJ_moneyrecord.loc[i]['money']-benchmark_moneyrecord.loc[i]['moneybenchmark']
    alpha.loc[i,'alpha']=alpha_i
KJ.plot_alpha(alpha,date_ls,startdate,enddate)
