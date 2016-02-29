# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:30:27 2016

@author: Liu
"""

from Show import show
import pandas as pd
from backtestA import leverageA
from KJmodel1223_2 import B

import os

def main():
    fn = os.path.join(os.path.dirname(__file__), 'data')
    #print fn
    
    df_nav = pd.read_csv(fn+'/NAVA.csv')
    df_b = pd.read_csv(fn+'/NAVB.csv')
    df_closeA=pd.read_csv(fn+'/closeA.csv')
    df_openA=pd.read_csv(fn+'/openA.csv')
    df_interest=pd.read_csv(fn+'/interestA.csv')
    df_m=pd.read_csv(fn+'/mA.csv')
    df_volume=pd.read_csv(fn+'/volumeA.csv')
    df_closeB=pd.read_csv(fn+'/closeB.csv')
    df_discount_ratio=pd.read_csv(fn+'/discount_ratio_M.csv')
    startdate="02/04/2015"
    enddate="20160205"
    
    capitalBase=1000000
    ratio=0.9
    capitalA=capitalBase*ratio
    capitalB=capitalBase*(1-ratio)
    
    
    leverage_algo=leverageA(df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,df_discount_ratio,'20150204',enddate,capitalA)
    #leverage_algo.set_pleverage_algo=leveragearameter(0.3,0.3)
    leverage_algo.backtest(0)
    pa=leverage_algo.portfolioValue
    #print pa
    
    K = 3
    J = 3

    KJ=B(capitalB,0,startdate,K,J)
    KJ_moneyrecord=KJ.test(startdate,K,J,capitalB,1,enddate)
    #benchmark_moneyrecord=KJ.benchtest(startdate,capitalB,enddate)
    pb=KJ_moneyrecord['money'].values.tolist()[:-1]    
    p=[x+y for x,y in zip(pa, pb)]
    
    
   
    #leverage_algoA=leverageA(df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,df_discount_ratio,'20150204',enddate,capitalBase)
    #leverage_algo.set_pleverage_algo=leveragearameter(0.3,0.3)
    #leverage_algoA.backtest(0)
    pa_base=[x / ratio for x in pa]
    
    #KJB=B(capitalBase,0,startdate,K,J)
    #KJB_moneyrecord=KJB.test(startdate,K,J,capitalBase,1,enddate)
    #benchmark_moneyrecord=KJ.benchtest(startdate,capitalB,enddate)
    pb_base=[x / (1-ratio) for x in pb]
 
    leverage_bench=leverageA(df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,df_discount_ratio,'20150204',enddate,capitalBase)
    #leverage_bench.backtest(1)
    result=show(leverage_algo,leverage_bench)
    result.plot3_pl(p,pa_base,pb_base)

    '''
    result.plot_cash(leverage_algo)    
    result.plot_pl()
    result.plot_alpha()
    result.plot_num(leverage_algo)
    result.plot_up(leverage_algo)
    result.plot_up(leverage_bench)
    result.plot_down(leverage_algo)
    result.plot_down(leverage_bench)
    print result.ratio()
    
    '''
    
if __name__=="__main__":
    main()