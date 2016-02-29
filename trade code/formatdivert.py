# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:21:18 2016

@author: Hansen Wang
"""
import pandas as pd
import os
fn = os.path.join(os.path.dirname(__file__), 'data')
def formatdivertBM(dfinitial):
    match=pd.read_csv(fn+'/Match.csv')
    sub=match['B'].tolist()
    sub.insert(0,"date")
    dfinitial.columns=sub
    del dfinitial[150320]
    del dfinitial[150334]
    del dfinitial[150352]
    del dfinitial[150354]
    del dfinitial[150286]
    del dfinitial[150350]
    del dfinitial[150240]
    del dfinitial[150254]
    del dfinitial[150358]
    del dfinitial[150314]
    return dfinitial
def formatdivertA(dfinitial):
    match=pd.read_csv(fn+'/Match.csv')
    sub=match['A'].tolist()#.insert(0,"date")
    sub.insert(0,'date')
    #print sub
    dfinitial.columns=sub
    #print dfinitial
    del dfinitial[150319]
    del dfinitial[150333]
    del dfinitial[150351]
    del dfinitial[150353]
    del dfinitial[150285]
    del dfinitial[150349]
    del dfinitial[150239]
    del dfinitial[150253]
    del dfinitial[150357]
    del dfinitial[150313]
    return dfinitial
    