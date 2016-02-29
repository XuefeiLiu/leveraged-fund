# -*- coding: utf-8 -*-

'''
代码缺陷：
缺失值得处理
'''

import numpy as np
import pandas as pd
from WindPy import w
from datetime import *
import datetime
import time
import threading
from threading import Thread

universe = ['150181','150171','150152','150227','150018','150235','150223','150117','150209','150200','150221',\
'502011','150184','150157','150130','150194','150196','150205','150051','150177','150261','150022','150243','150123',\
'150211','502004','150231','150192','150265','150100','150343','150219','502049','150096','150203','150329','150085',\
'150198','150303','150299','150106','150335','150190','150186','150275','150301','150173','150291','150315','502037',\
'150217','150241','150251','150317','502054','502007','150289','150325','150277','150295','150028','150179','150012',\
'150281','150321','150269','150150','150213','150207','150247','150287','150229','150225','502057','150249','150059',\
'150267','502014','150323','150255','150237','150305','150331','150259','502031','150148','150307','150245','150215',\
'150297','150030','150283','150309','150108','150311','150273','150083','150257','150135','150090','150293','150279',\
'150327','150104','502041','150233','150167','150008','150271','150140','150112','150057','502024','150094','150073',\
'502021','150263','150088','502001','150076','150138','150053','150145','150121','150092','150064','502017','150055',\
'150285','150349','150239','150253','150357','150313','502027','150319','150333','150351','150353']


        
      
        
def func1():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_navA = pd.read_csv('NAVA.csv')
    last_date_navA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_navA.iloc[-1,0])),"%Y%m%d"))
    day_gap_navA = w.tdayscount(last_date_navA, yesterday).Data[0][0]-1
    print 1
    stock_ls=[]
    w_wsd_data={}
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock += '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'nav',   (w.tdaysoffset(1,last_date_navA).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
       
    for i in xrange(day_gap_navA):
        
        this_day = w.tdaysoffset(i+1,last_date_navA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")

          
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
        f=open('NAVA.csv','a')
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
def func2():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_openA=pd.read_csv('openA.csv')
    last_date_openA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_openA.iloc[-1,0])),"%Y%m%d"))
    day_gap_openA = w.tdayscount(last_date_openA, yesterday).Data[0][0]-1
    print 2
    w_wsd_data={}
    stock_ls=[]
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock += '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'open',  (w.tdaysoffset(1,last_date_openA).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
      
    for i in xrange(day_gap_openA):
        
        this_day = w.tdaysoffset(i+1,last_date_openA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")

        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
            
        f=open('openA.csv','a')
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
def func3():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")     
    df_closeA=pd.read_csv('closeA.csv')
    last_date_closeA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_closeA.iloc[-1,0])),"%Y%m%d"))
    day_gap_closeA = w.tdayscount(last_date_closeA, yesterday).Data[0][0]-1
    print 3
    stock_ls=[]
    w_wsd_data={}
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock += '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'close', (w.tdaysoffset(1,last_date_closeA).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
        
    for i in xrange(day_gap_closeA):

        this_day = w.tdaysoffset(i+1,last_date_closeA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")


        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
            
        f=open('closeA.csv','a')   
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
def func4():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")     
    df_interestA=pd.read_csv('interestA.csv')
    last_date_interestA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_interestA.iloc[-1,0])),"%Y%m%d"))
    day_gap_interestA = w.tdayscount(last_date_interestA, yesterday).Data[0][0]-1
    print 4
    w_wsd_data={}
    stock_ls=[]
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock += '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'fund_agreedannuyield', (w.tdaysoffset(1,last_date_interestA).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
    for i in xrange(day_gap_interestA):
        this_day = w.tdaysoffset(i+1,last_date_interestA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
        f=open('interestA.csv','a') 
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
    
def func5():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_volumeA=pd.read_csv('volumeA.csv')
    last_date_volumeA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_volumeA.iloc[-1,0])),"%Y%m%d"))
    print last_date_volumeA
    day_gap_volumeA = w.tdayscount(last_date_volumeA, yesterday).Data[0][0]-1
    print day_gap_volumeA
    stock_ls=[]
    w_wsd_data={}
    start=(w.tdaysoffset(1,last_date_volumeA).Data[0][0]).strftime("%Y-%m-%d")
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock += '.SH'
        stock_ls.append(stock)
        #start=w.tdaysoffset(1,last_date_volumeA)
        w_wsd_data[stock] = w.wsd(stock, 'volume',start  ,yesterday)
    print w_wsd_data
    for i in xrange(day_gap_volumeA):

        this_day = w.tdaysoffset(i+1,last_date_volumeA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
        f=open('volumeA.csv','a')  
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
def func6():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_closeB=pd.read_csv('closeB.csv')
    last_date_closeB = time.strftime("%Y-%m-%d",time.strptime(str(int(df_closeB.iloc[-1,0])),"%Y%m%d"))
    day_gap_closeB = w.tdayscount(last_date_closeB, yesterday).Data[0][0]-1
    print 6
    w_wsd_data={}
    stock_ls=[]
    for stock in universe:
        if stock =='150073':
            stock='150075.SZ'
        else:
            if stock[0]=='1':
                stock = str(int(stock[:6])+1) + '.SZ'
            else:
                stock = str(int(stock[:6])+1) + '.SH'
        stock_ls.append(stock)

        w_wsd_data[stock] = w.wsd(stock, 'close',  (w.tdaysoffset(1,last_date_closeB).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
       # print 1
        print stock
        #if w_wsd_data[stock].Data[0][0]==None:
    for i in xrange(day_gap_closeB):
  
        this_day = w.tdaysoffset(i+1,last_date_closeB)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
            
        f=open('closeB.csv','a')   
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
        
    print 'finish'
    
def func7():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_navB = pd.read_csv('NAVB.csv')
    last_date_navB = time.strftime("%Y-%m-%d",time.strptime(str(int(df_navB.iloc[-1,0])),"%Y%m%d"))
    day_gap_navB = w.tdayscount(last_date_navB, yesterday).Data[0][0]-1    
    print 7
    w_wsd_data={} 
    stock_ls=[]
    for stock in universe:
        if stock =='150073':
            stock='150075.SZ'
        else:
            if stock[0]=='1':
                stock = str(int(stock[:6])+1) + '.SZ'
            else:
                stock = str(int(stock[:6])+1) + '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'nav',  (w.tdaysoffset(1,last_date_navB).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
    for i in xrange(day_gap_navB):
        
        this_day = w.tdaysoffset(i+1,last_date_navB)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
           
        f=open('NAVB.csv','a')      
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
   
def func8():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_mA = pd.read_csv('mA.csv')
    last_date_mA = time.strftime("%Y-%m-%d",time.strptime(str(int(df_mA.iloc[-1,0])),"%Y%m%d"))
    day_gap_mA = w.tdayscount(last_date_mA, yesterday).Data[0][0]-1
    w_wsd_data={}
    print 8
    stock_ls=[]
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock = stock + '.SH'

        mA_code = w.wsd(stock, 'fund_smfcode', yesterday).Data[0][0]
        stock_ls.append(mA_code)
        w_wsd_data[mA_code] = w.wsd(mA_code, 'nav', (w.tdaysoffset(1,last_date_mA).Data[0][0]).strftime("%Y-%m-%d"),yesterday)  

    for i in xrange(day_gap_mA):
        this_day = w.tdaysoffset(i+1,last_date_mA)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
        f=open('mA.csv','a') 
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'

def func9():
    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_discount_ratio_M = pd.read_csv('discount_ratio_M.csv')
    last_date_discount_ratio_M = time.strftime("%Y-%m-%d",time.strptime(str(int(df_discount_ratio_M.iloc[-1,0])),"%Y%m%d"))
    day_gap_discount_ratio_M = w.tdayscount(last_date_discount_ratio_M, yesterday).Data[0][0]-1
    w_wsd_data={}
    print 9
    stock_ls=[]
    for stock in universe:
        if stock[0]=='1':
            stock = stock + '.SZ'
        else:
            stock = stock + '.SH'

        mA_code = w.wsd(stock, 'fund_smfcode', yesterday).Data[0][0]
        stock_ls.append(mA_code)
        w_wsd_data[mA_code] = w.wsd(mA_code, 'anal_tdiscountratio', (w.tdaysoffset(1,last_date_discount_ratio_M).Data[0][0]).strftime("%Y-%m-%d"),yesterday)  
    for i in xrange(day_gap_discount_ratio_M):
        this_day = w.tdaysoffset(i+1,last_date_discount_ratio_M)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
        f=open('discount_ratio_M.csv','a') 
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'

def func10():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_openB=pd.read_csv('openB.csv')
    last_date_openB = time.strftime("%Y-%m-%d",time.strptime(str(int(df_openB.iloc[-1,0])),"%Y%m%d"))
    day_gap_openB = w.tdayscount(last_date_openB, yesterday).Data[0][0]-1
    print 10
    w_wsd_data={}
    stock_ls=[]
    for stock in universe:
        if stock =='150073':
            stock='150075.SZ'
        else:
            if stock[0]=='1':
                stock = str(int(stock[:6])+1) + '.SZ'
            else:
                stock = str(int(stock[:6])+1) + '.SH'
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'open',  (w.tdaysoffset(1,last_date_openB).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
       # print 1
        #if w_wsd_data[stock].Data[0][0]==None:
    for i in xrange(day_gap_openB):
  
        this_day = w.tdaysoffset(i+1,last_date_openB)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
            
        f=open('openB.csv','a')   
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
        f.close()
    print 'finish'
    
def func11():
    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d") 
    df_industry=pd.read_csv('industry.csv')
    last_date_industry = time.strftime("%Y-%m-%d",time.strptime(str(int(df_industry.iloc[-1,0])),"%Y%m%d"))
    day_gap_industry = w.tdayscount(last_date_industry, yesterday).Data[0][0]-1
    print 11
    w_wsd_data={}
    stock_ls=[]
    for stock in list(df_industry.columns.values)[1:]  :
        stock_ls.append(stock)
        w_wsd_data[stock] = w.wsd(stock, 'close',  (w.tdaysoffset(1,last_date_industry).Data[0][0]).strftime("%Y-%m-%d"),yesterday)
        print w_wsd_data
    f=open('industry.csv','a')   
    for i in xrange(day_gap_industry):
  
        this_day = w.tdaysoffset(i+1,last_date_industry)
        ls = []
        this_day_csv = (this_day.Data[0][0]).strftime("%Y%m%d")
        for stock in stock_ls:
            ls.append(w_wsd_data[stock].Data[0][i])  
            
        
        f.write(this_day_csv)
        for stock_data in ls:
            f.write(",")
            f.write(str(stock_data))
        f.write("\n")
    f.close()
        
    print 'finish'
    

def main():
    w.start()
    func1()
    func2()
    func3()
    func4()
    func5()
    func6()
    func7()
    func8()
    func9()
    func10()
    func11()
    #a=w.wsd('150074.SZ', 'nav','2015-12-11','2015-12-22')
    #print a    
    #a=w.wsd('502022.SH', 'nav','2015-12-11','2015-12-22')
    #print a  
    '''
    Thread(target = func1).start()
    Thread(target = func2).start()
    Thread(target = func3).start()
    Thread(target = func4).start()
    Thread(target = func5).start()
    Thread(target = func7).start()
    Thread(target = func8).start()
    '''
    
if __name__=="__main__":
    main()