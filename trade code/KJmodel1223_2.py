# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 14:05:00 2015

@author: Hansen Wang
"""

#本版本加入了涨跌停板不能买入的问题，以及加入接近下折则不买入的阈值
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from formatdivert import formatdivertBM, formatdivertA
import os

fn = os.path.join(os.path.dirname(__file__), 'data')
df_A_nav=pd.read_csv(fn+'/NAVA.csv')
#print(df_A_nav.columns)
df_A_nav=formatdivertA(df_A_nav)
date_ls = df_A_nav['date'].tolist()

date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])
date_ls.remove(date_ls[-1])

#print(date_ls)
date_ls_total = df_A_nav['date'].tolist()

df_A_nav=df_A_nav.set_index(['date'])

df_industry = pd.read_csv(fn+'/industry.csv')
df_industry.index=df_industry['date']

df_B_close = pd.read_csv(fn+'/closeB.csv')
df_B_close=formatdivertBM(df_B_close)
df_B_close=df_B_close.set_index(['date'])

df_M_NAV = pd.read_csv(fn+'/mA.csv')
df_M_NAV=formatdivertBM(df_M_NAV)
df_M_NAV=df_M_NAV.set_index(['date'])

df_A_ratio = pd.read_csv(fn+'/A_ratio.csv')
df_A_ratio=df_A_ratio.set_index(['code'])


df_M_discount = pd.read_csv(fn+'/discount_ratio_M.csv')
df_M_discount=formatdivertBM(df_M_discount)
df_M_discount=df_M_discount.set_index(['date'])

df_A_close=pd.read_csv(fn+'/closeA.csv')
df_A_close=formatdivertA(df_A_close)
df_A_close=df_A_close.set_index(['date'])

df_A_interest=pd.read_csv(fn+'/interestA.csv')
df_A_interest=formatdivertA(df_A_interest)
df_A_interest=df_A_interest.set_index(['date'])
#print(df_A_interest.index)

df_B_nav=pd.read_csv(fn+'/NAVB.csv')
df_B_nav=formatdivertBM(df_B_nav)
df_B_nav=df_B_nav.set_index(['date'])
#print(df_B_nav.index)

df_B_open=pd.read_csv(fn+'/openB.csv')
df_B_open=formatdivertBM(df_B_open)
df_B_open.index=df_B_open['date']

df_bankuai_jijin=pd.read_csv(fn+'/Bankuai-jijindaima.csv')
#print(df_bankuai_jijin)

class B():
    cash = []
    account = []
    
    def __init__(self,cash,account,startdate,K,J):
        self.cash = cash
        self.account = account
        self.startdate = startdate
        self.K=K
        self.J=J
        
#跟踪每次交易持仓变化  
    def buy(self,code,date,account,cash,number):  
        price=df_B_open.loc[int(date)][int(code)]
        #print(df_B_open)
        print(code)
        print(date)
        #print(price)
        #print(type(cash))
        #print(number)
        #print(cash)
        #print(cash/price/number)
        account.loc[str(code)]['hand']+=float(cash)/float(price)/int(number)
        #print (code)
        #print (date)
        return account
    def sell(self,code,account):
        account.loc[str(code)]['hand']=0
        return account
#跟踪每次交易手中现金变化
    def buyloss(self,cashinhand,cash,number):
        return (cashinhand-cash/number)
    def sellgain(self,code,date,account,cashinhand):
        price=df_B_open.loc[int(date)][int(code)]
        hand=account.loc[str(code)]['hand']
        #print(price)
        #print(type(price))
        
        return (cashinhand+float(price)*hand)
#计算每日account内资金额
    def accountmoney(self,date,account,cashinhand):
        #print(cashinhand)
        accountmoney=0
        #print(account)
        #print(df_B_close[502005])
        for i in account.index:
            #print(type(i))
            #print(date)
            price=df_B_close.loc[int(date)][int(i)]
            '''
            if date=='20150522':            
                print(price)
            '''
            accountmoney+=price*account.loc[i]['hand']
        #print(accountmoney)
        a=accountmoney+cashinhand
        return a
        
#构造一个转换日期格式的函数,从mm/dd/yyyy转化成yyyymmdd
    def datetransfer(self,date):
        timeArray_date=time.strptime(date,"%m/%d/%Y")
        date_transfered=time.strftime("%Y%m%d",timeArray_date)
        return date_transfered
#构造一个转换日期格式的函数,从yyyymmdd转化成mm/dd/yyyy        
    def datetransferback(self,date):
        timeArray_date=time.strptime(date,"%Y%m%d")
        date_transfered=time.strftime("%m/%d/%Y",timeArray_date)
        return date_transfered
#构造一个直接能将字符式日期加减的函数    
    def datecal(self,start,daysdelta):
        timeArray_start=time.strptime(start,"%m/%d/%Y")
        timeStamp_start=int(time.mktime(timeArray_start))
        dateArray_start = datetime.datetime.utcfromtimestamp(timeStamp_start)
        dateArray_end=dateArray_start+datetime.timedelta(days=daysdelta)
        datestr_end=dateArray_end.strftime("%m/%d/%Y")
        return datestr_end
#凑造一个能直接加减几个交易日的函数,输入的初始日期采用20151030格式
    def tradedatecal(self,start,daysdelta,tradedate_ls):
        i=0
        if daysdelta>0:
            for j in range(2,1000):
                timeArray_start=time.strptime(str(start),"%Y%m%d")
                timeStamp_start=int(time.mktime(timeArray_start))
                dateArray_start = datetime.datetime.utcfromtimestamp(timeStamp_start)
                dateArray_end=dateArray_start+datetime.timedelta(days=j)
                datestr_end=dateArray_end.strftime("%Y%m%d")
                if int(datestr_end) in tradedate_ls:
                    i+=1
                if i==daysdelta:
                    break
        if daysdelta<0:
            for j in range(0,1000):
                timeArray_start=time.strptime(str(start),"%Y%m%d")
                timeStamp_start=int(time.mktime(timeArray_start))
                dateArray_start = datetime.datetime.utcfromtimestamp(timeStamp_start)
                dateArray_end=dateArray_start+datetime.timedelta(days=-j)
                datestr_end=dateArray_end.strftime("%Y%m%d")
                if int(datestr_end) in tradedate_ls:
                    i-=1
                if i==daysdelta:
                    break
        return datestr_end
#构建一个搜寻与给定日期最相近的交易日（首先只写向后搜寻）
    def tradedatesearch(self,date):
        for i in range(1,30):
            searchdate=self.datecal(date,i)
            #print(searchdate)
            flag=0            
            for j in df_industry['date'] :           
                if searchdate==j:
                    flag=1
                    break
                else:
                    continue
            if flag==1:
                break
            else:
                continue
        return searchdate

#向前搜寻最近的交易日        
    def tradedatesearchback(self,date):
        for i in range(30):
            searchdate=self.datecal(date,-i)
            #print(searchdate)
            flag=0            
            for j in df_industry['date'] :           
                if searchdate==j:
                    flag=1
                    break
                else:
                    continue
            if flag==1:
                break
            else:
                continue
        return searchdate

#整理可交易的时间，形成列表 
    def feasibledate(self,startdate,enddate,K,J):
        #首先调成时间数组形式
        timeArray_start = time.strptime(startdate,"%m/%d/%Y")
        timeArray_end = time.strptime(enddate,"%m/%d/%Y")
        #获得时间戳
        timeStamp_start = int(time.mktime(timeArray_start))
        timeStamp_end = int(time.mktime(timeArray_end))
        buy_months=int(((timeStamp_end-timeStamp_start)/3600/24-K)/J)
        #print(buy_months)
        #构建买入日期列表list
        ls_dates = []
        for i in range(buy_months+1):
            buy_month_str=self.datecal(startdate,(K+J*i))
            buy_month_str=self.tradedatesearch(buy_month_str)
            #print(buy_month_str)
            ls_dates.append(buy_month_str)
        return ls_dates
#对每一次交易时的板块进行排名并取前五个        
    def rank(self,buy_date,K):
        stock_profit_dict={'stocks':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],'profit':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
        stock_profit_df=pd.DataFrame(stock_profit_dict)
        for i in range(1,21):
            initialtime_str=self.tradedatecal(buy_date,-K,date_ls_total)
            #print(initialtime_str)
            price1=df_industry.loc[int(initialtime_str)][i]
            price2=df_industry.loc[buy_date][i]
            profit=(price2-price1)/price1
            stock_profit_df.ix[i-1,1]=i
            stock_profit_df.ix[i-1,0]=profit
        stock_profitorder_df=stock_profit_df.sort(columns='profit')
        portfolio_dict={'stocks':[0,0,0,0,0,0,0,0,0,0]}
        portfolio_df=pd.DataFrame(portfolio_dict)
        for j in range (10):           
            portfolio_df.ix[j,0]=stock_profitorder_df.iloc[19-j][1]
        #print(portfolio_df)
        return portfolio_df
               
#对于每一个K，输出最后的板块排名
    def Krank(self,startdate,enddate,K,J):
         stock_krank_dict = {'stocks':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],'score':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
         stock_krank_df = pd.DataFrame(stock_krank_dict)
         ls_kdate = self.feasibledate(startdate, enddate, K,J)
         #print(ls_kdate)
         for i in ls_kdate:
             portfolio_krank = self.rank(i,K)
             for j in range(5):
                    for s in range(1,21):
                        if portfolio_krank.ix[j,'stocks'] == s:
                            stock_krank_df.ix[s-1,'score']  += 5-j
                            stock_finalkrank_df = stock_krank_df.sort(columns='score')
         order_dict={'stocks':[0,0,0,0,0]}
         order_df=pd.DataFrame(order_dict)
         for m in range (5):           
             order_df.ix[m,0]=stock_finalkrank_df.iloc[19-m][1]
         print (order_df)
         return order_df
         
#计算A的理论价格
    def irr_mean(self,stocklist,date):
        irr={}
    #选股时不考虑下折的分级A（不能买入），只有当其净值不为1时才考虑，全部按照永续计算。
    #基于昨天的收盘价得出的隐含收益率
        for stock in stocklist:
            if df_A_close.loc[int(date)][int(stock)]:
                #p = self.referencePrice[stock]
                p=df_A_close.loc[int(date)][int(stock)]
                interest = df_A_interest.loc[int(date)][int(stock)]
                nav = df_A_nav.loc[int(date)][int(stock)]
                irr[int(stock)] = interest/(p-(nav-1))
            else:
                continue

        stock_ls=[]
        for key in irr:
            stock_ls.append(irr[key])

        irr_mean = sum(stock_ls) / len(stock_ls)
        return irr_mean         

    def fv_pA (self,code,date):
        universe2 =['150209','150171','150181','150194','150130','150227','150152','150184','502004','502011','150018','150051','150221','502007','150205','150261','150277','150235','150303','150177']
        irr=self.irr_mean(universe2, date)
        #print (date)
        interest=df_A_interest.loc[int(date)][int(code)]
        nav=df_A_nav.loc[int(date)][int(code)]
        #date_days_later = date_ls[date_ls.index(date)+day]
        P_A0 = interest / irr + (nav -1)
        P_A0_days_later = interest / irr 
        P_A1 = (nav  - 0.25) * 1 + 0.25 * P_A0_days_later
        navB = df_B_nav.loc[int(date)][int(str(int(code[:6])+1)+code[6:])]
    
        #para = fit_curve (day)
        #p = func (navB, para[0], para[1], para[2], para[3])
        p = self.func (navB, 31.2,  -15.07, 0.3931,  -1.115)
        return p * P_A1 + (1 - p) * P_A0  

    def func(self,x, a, b, c, d):
        return a*np.exp(b*x) + c*np.exp(d*x)
    
#计算B的理论价格
    def pricingB (self,code,date):
        A_ratio = df_A_ratio.loc[(int(code)-1)]['ratio']
        priceA=self.fv_pA(str(int(code)-1),date)
        m_nav = df_M_NAV.loc[int(date)][int(code)]
        m_discount = df_M_discount.loc[int(date)][int(code)]
        #print(m_nav)
        #print(type(m_nav))
        #print(m_discount)
        #print(type(m_discount))
        #print(A_ratio)
        #print(type(A_ratio))
        #print(priceA)
        #print(type(priceA))
        #print(A_ratio*priceA)
        price_B = (float(m_nav)*(m_discount+1) - A_ratio*priceA)/(1-A_ratio)
        #print (df_priceB)
        return price_B
        '''        
        #取出交易时间,后面的dataframe都是读进来的表格；A的价格相应函数用priceA表示
        ls_tradedate = df_B_close.index
        print(ls_tradedate)
        #print(code)
        #print(str(int(code)-1))
        A_ratio = df_A_ratio.loc[(int(code)-1)]['ratio']
        df_priceB = pd.DataFrame()
        for i in ls_tradedate:
            priceA=self.fv_pA(str(int(code)-1),i)
            m_nav = df_M_NAV.loc[int(i)][str(int(code))]
            m_discount = df_M_discount.loc[int(i)][str(int(code))]
            price_B = (m_nav*(m_discount+1) - A_ratio*priceA)/(1-A_ratio)
            df_priceB.loc[i,'priceB'] = price_B        
        #print (df_priceB)
        return df_priceB   
        '''   
    
#对分级B的ratio=（理论价格-实际价格）/理论价格进行排名选取前三只
    def fundrank(self,date,K,number):
        flag=0
        ratio_df=pd.DataFrame(columns=['code','ratio'])
        portfolio_df=self.rank(date,K)
        #print(portfolio_df)
        for i in portfolio_df['stocks']:
            jijin_ls=df_bankuai_jijin[str(int(i))]
            for j in jijin_ls:
                #print(j)
                if j<600000 and j>100000:                                  
                    priceB_real=df_B_close.loc[int(date)][int(j)]
                    if priceB_real!=0:
                        ratio_df.loc[flag,'code']=int(j)
                        priceB_theory=self.pricingB(j,date)
                        a=-(priceB_theory-priceB_real)/priceB_theory
                        ratio_df.loc[flag,'ratio']=a
                        flag+=1
                else:
                    break
        ratio_df=ratio_df.sort(columns='ratio')
        #print(ratio_df)
        fund_firstthree_df=pd.DataFrame()
        for k in range(number):
            fund_firstthree_df.loc[k,'code']=ratio_df.iloc[k]['code']
        #print(fund_firstthree_df)
        return fund_firstthree_df
#定义判断给定日期是否为上折日的函数
    def shangzhedate(self,stock,date,date_ls):
        flag = 0
        date1=self.tradedatecal(date,1,date_ls) 
        date_1=self.tradedatecal(date,-1,date_ls)  
      

        nav0 = float(df_B_nav.loc[int(date)][int(stock)])
        nav1 = float(df_B_nav.loc[int(date1)][int(stock)])
        nav_1 = float(df_B_nav.loc[int(date_1)][int(stock)])

        price0 = df_B_close.loc[int(date)][int(stock)]
        price1 = df_B_close.loc[int(date1)][int(stock)]
        price_1 = df_B_close.loc[int(date_1)][int(stock)]

            
        if price0 == price1:
            if nav_1 > 1.95 and nav0 <1.2:
                flag = 1
            elif nav0>1.95 and nav1<1.2:
                flag=1
        return flag
#定义判断是否为下折日的函数     
    def xiazhedate(self,stock,date,date_ls):
        flag = 0
        date1=self.tradedatecal(date,1,date_ls)  
        date_1=self.tradedatecal(date,-1,date_ls)
         

        nav0 = float(df_B_nav.loc[int(date)][int(stock)])
        nav1 = float(df_B_nav.loc[int(date1)][int(stock)])
        nav_1 = float(df_B_nav.loc[int(date_1)][int(stock)])

        price0 = df_B_close.loc[int(date)][int(stock)]
        price1 = df_B_close.loc[int(date1)][int(stock)]
        price_1 = df_B_close.loc[int(date_1)][int(stock)]

            
        if price0 == price1:
            if nav_1 <0.3 and nav_1!=0 and nav0 >0.9:
                flag = 1
            elif nav0<0.3 and nav0!=0 and nav1>0.9:
                flag=1
        return flag
#停盘日返回1，非停盘日返回0   
    def stoptradedate(self, stock, date,date_ls):
        flag = 0;
        date_1=self.tradedatecal(date,-1,date_ls)
        if self.shangzhedate(stock,date_1,date_ls) == 1:
            flag = 1
        elif self.xiazhedate(stock,date_1,date_ls) ==1:
            flag = 1
        return flag
        
#判断是否涨跌停
    def zhangting(self,stock,date):
        priceopen=df_B_open.loc[date][int(stock)]
        date_1=self.tradedatecal(date,-1,date_ls_total)
        priceclose=df_B_close.loc[int(date_1)][int(stock)]
        if priceopen>1.095*priceclose:
            flag=1
        else:
            flag=0
        return(flag)
        
    def dieting(self,stock,date):
        priceopen=df_B_open.loc[date][int(stock)]
        date_1=self.tradedatecal(date,-1,date_ls_total)
        priceclose=df_B_close.loc[int(date_1)][int(stock)]
        if priceopen<0.905*priceclose:
            flag=1
        else:
            flag=0
        return(flag)

#判断上下折停盘之后是否涨跌停
    def zhangtingzhesuan(self,stock,date):
        if df_B_open.loc[date][int(stock)]>1.095:
            flag=1
        else:
            flag=0
        return (flag)
            
    def dietingzhesuan(self,stock,date):
        if df_B_open.loc[date][int(stock)]<0.905:
            flag=1
        else:
            flag=0
        return (flag)
               
#给定portfolio进行回测
    def test(self,startdate,K,J,cash,number,enddate):
        #建立account_df初始状态
        account_df=pd.DataFrame()     
        for i in range(1,21):
            Bcode_ls=df_bankuai_jijin[str(int(i))]
            for j in Bcode_ls:
                if j<600000 and j>100000:
                    account_df.loc[str(int(j)),'hand']=0
        #print(account_df)
        #给定cashinhand初始状态，即等于最开始给定的cash
        cashinhand=cash
        #建立一个dateflag跟踪是否是第一次交易
        dateflag=0
        #建立一个dateintervalflag跟踪每J天进行的一次交易
        dateintervalflag=1
        #建立记录所需list和日期
        buy_daterecord=self.datetransfer(self.datecal(startdate,0))
        buy_coderecord=[]
        sell_daterecord=self.datetransfer(self.datecal(startdate,0))
        sell_coderecord=[]
        shangzhe_daterecord=self.datetransfer(self.datecal(startdate,0))
        shangzhe_coderecord=[]
        xiazhe_daterecord=self.datetransfer(self.datecal(startdate,0))
        xiazhe_coderecord=[]
        
        buytingban_coderecord=[]
        selltingban_coderecord=[]
        #确定初始交易日
        startdate=self.datetransfer(startdate)
        firsttrade=self.tradedatecal(startdate,K,date_ls_total)
        print(firsttrade)
        #print(type(firsttrade))
        
        #定义总体持仓列表
        total_portfolio=pd.DataFrame() 
        #定义总资产列表
        moneyrecord_df=pd.DataFrame()
        #print(date_ls)
        #对于所有开盘日进行一个循环
        for i in date_ls:

                #对每一天各个记录的list进行计数            
                count_buy=0
                count_shangzhe=0
                count_xiazhe=0

                for s in buy_coderecord:
                    if self.zhangting(s,i)!=1:
                        count_buy+=1
                for s in buytingban_coderecord:
                    if self.zhangting(s,i)!=1:
                        count_buy+=1

                for s in shangzhe_coderecord:
                    count_shangzhe+=1
                for s in xiazhe_coderecord:
                    count_xiazhe+=1

                    #每天先进行一个判断，今天是否已经到了持仓的基金上折返现或者下折手数变化的日期，之所以先判断这个是为了防止有的基金在上折之后停盘日被选择卖出，这样可以先回收利润，然后再卖出，如果下折可以先修改手数，然后卖出，符合实际
                if i==int(shangzhe_daterecord):
                    #print(i)
                    #print("premium")
                    #print(cashinhand)
                    datebefore=self.tradedatecal(shangzhe_daterecord,-3,date_ls_total)
                    #print(datebefore)
                    #print(type(datebefore))
                    for s in shangzhe_coderecord:
                        navB1=df_B_nav.loc[int(datebefore)][int(s)]
                        navB2=df_B_nav.loc[int(shangzhe_daterecord)][int(s)]
                        cashinhand+=(navB1-navB2)*account_df.loc[str(s)]['hand']
                    shangzhe_coderecord=[]
                if i==int(xiazhe_daterecord):
                    #print(i)
                    #print("discount")
                    #print(cashinhand)
                    datebefore=self.tradedatecal(xiazhe_daterecord,-3,date_ls_total)
                    for s in xiazhe_coderecord:
                        navB1=df_B_nav.loc[int(datebefore)][int(s)]
                        navB2=df_B_nav.loc[int(xiazhe_daterecord)][int(s)]
                        account_df.loc[str(s)]['hand']=account_df.loc[str(s)]['hand']*navB1/navB2
                    xiazhe_coderecord=[]
                    #print(cashinhand)
                    
                #卖出之前因为跌停板无法卖出但今天终于能卖出的
                for s in selltingban_coderecord:
                    if self.dieting(s,i)!=1:
                        cashinhand=self.sellgain(s,i,account_df,cashinhand)                        
                        account_df=self.sell(s,account_df)
                        selltingban_coderecord.remove(s)
                        
                #每天再进行一个判断，是否是之前买卖因为停盘没有实现？若是，进行买卖        
                if i==int(sell_daterecord):
                    for s in sell_coderecord:
                        if self.dietingzhesuan(s,i)!=1:
                            cashinhand=self.sellgain(s,i,account_df,cashinhand)                        
                            account_df=self.sell(s,account_df)
                            #print(account_df)
                        else:
                            selltingban_coderecord.append(int(s))
                    sell_coderecord=[]                
                        
                #买入之前因为涨停板无法买入但今天终于能买入的
                cash_buy=cashinhand
                #print(buytingban_coderecord)
                for s in buytingban_coderecord:
                    if self.zhangting(s,i)!=1:
                        account_df=self.buy(s,i,account_df,cash_buy,count_buy)
                        cashinhand=self.buyloss(cashinhand,cash_buy,count_buy)
                        buytingban_coderecord.remove(s)
                
                if i==int(buy_daterecord):
                    #每次买入时候都要记录两个关键数值，现有手中总钱数，和这次买入总基金数
                    for s in buy_coderecord:
                        if self.zhangtingzhesuan(s,i)!=1:
                            account_df=self.buy(s,i,account_df,cash_buy,count_buy)
                            cashinhand=self.buyloss(cashinhand,cash_buy,count_buy)
                        else:
                            buytingban_coderecord.append(s)
                    buy_coderecord=[]
                

                #每个交易日分成两种情况，第一次交易和之后的交易，这里是第一次交易
                if dateflag==0:
                    #print(i)
                    #print(type(i))
                    #判断是否是第一个交易日，如果是的话进行交易
                    if i==int(firsttrade):
                        buyinitial_df=self.fundrank(i,K,number)
                        #print(buyinitial_df)
                        total_portfolio=pd.concat([total_portfolio,buyinitial_df],axis=1)
                        cash_buy=cashinhand
                        #对要购买的组合中每一只都进行判断当天是否为停盘日，若为停盘日，则需下一天购买
                        numberbuy=number                        
                        for j in buyinitial_df['code']:
                            #print(i)
                            #print(type(i))
                            #print(j)
                            #print(type(j))
                            #print(df_B_nav)
                            #print(int(j))
                            #print(df_B_nav.loc[i][int(j)])
                            if df_B_nav.loc[int(i)][int(j)]<0.3 and self.stoptradedate(int(j),i,date_ls_total)!=1:
                                numberbuy-=1
                        #print(numberbuy)
                        for j in buyinitial_df['code']:
                            #print(int(j))
                            #如果是停盘日
                            if self.stoptradedate(int(j),i,date_ls_total)==1:
                                #记录下一天为购买日,记录需要购买的基金号
                                buy_daterecord=self.tradedatecal(i,1,date_ls_total)
                                buy_coderecord.append(int(j))
                            else:
                                #写一个buyloss函数计算买入cashinhand的变化结果
                                if df_B_nav.loc[i][int(j)]>=0.3:
                                    if self.zhangting(j,i)!=1:
                                        account_df=self.buy(int(j),i,account_df,cash_buy,numberbuy)
                                        cashinhand=self.buyloss(cashinhand,cash_buy,numberbuy)
                                    else:
                                        buytingban_coderecord.append(int(j))
                            dateflag+=1
                            #print(account_df)
                        #print(cashinhand)
                    #如果不是第一个交易日
                else:
                    #如果持仓到达了J天，则进行买卖
                    if dateintervalflag==J:
                        #print("sellbuy")
                        #print(i)
                        #首先卖出能卖出的基金
                        for j in account_df.index:
                            #如果是停盘日，就保留代号和日期之后再卖
                            if account_df.loc[j]['hand']!=0:
                                if (self.stoptradedate(j,i,date_ls_total)==1):
                                    sell_daterecord=self.tradedatecal(i,1,date_ls_total)
                                    sell_coderecord.append(int(j))
                                else:
                                    if self.dieting(j,i)!=1:
                                        #写一个sellgain函数计算每次卖出cashinhand的变化结果
                                        cashinhand=self.sellgain(j,i,account_df,cashinhand)
                                        account_df=self.sell(j,account_df)
                                        #print(cashinhand)
                                    else:
                                        selltingban_coderecord.append(int(j))
                        #print(account_df)
                        #再买入能买入的基金
                        buy_df=self.fundrank(i,K,number)
                        total_portfolio=pd.concat([total_portfolio,buy_df],axis=1)
                        cash_buy=cashinhand
                        numberbuy=number                        
                        for j in buy_df['code']:
                            if df_B_nav.loc[i][int(j)]<0.3 and self.stoptradedate(int(j),i,date_ls_total)!=1:
                                numberbuy-=1
                        for j in buy_df['code']:
                            #如果是停盘日
                            if (self.stoptradedate(int(j),i,date_ls_total)==1):
                                #记录下一天为购买日,记录需要购买的基金号
                                buy_daterecord=self.tradedatecal(i,1,date_ls_total)
                                buy_coderecord.append(int(j))
                                #print(i)
                            else:
                                #写一个buyloss函数计算买入cashinhand的变化结果
                                #if i==20150522:
                                    #print(cashinhand)
                                if df_B_nav.loc[i][int(j)]>=0.3:
                                    if self.zhangting(j,i)!=1:
                                        account_df=self.buy(int(j),i,account_df,cash_buy,numberbuy)
                                        cashinhand=self.buyloss(cashinhand,cash_buy,numberbuy)
                                    else:
                                        buytingban_coderecord.append(int(j))
                                #if i==20150522:
                                    #print(account_df)
                        #print(account_df)
                        dateintervalflag=1
                    #如果没有达到J天，则把计数加一
                    else:
                        dateintervalflag+=1
                    #不论是否交易，都需要检验在当天最终获得的仓位中基金是否发生上下折，如果发生需要在之后返还现金或者更该手数
                    for k in account_df.index:
                        if account_df.loc[k]['hand']!=0 and self.shangzhedate(k,i,date_ls_total)==1:
                            #print("shangzhe")
                            #print(i)
                            #print(type(i))
                            #print(k)
                            shangzhe_daterecord=self.tradedatecal(i,2,date_ls_total)
                            #print(shangzhe_daterecord)
                            shangzhe_coderecord.append(k)
                        if account_df.loc[k]['hand']!=0 and self.xiazhedate(k,i,date_ls_total)==1:
                            #print("xiazhe")
                            #print(i)
                            #print(k)
                            xiazhe_daterecord=self.tradedatecal(i,2,date_ls_total)
                            xiazhe_coderecord.append(k)
                #记录每日总资产
                #print(cashinhand)
                #print (int(i))
                #print (int(startdate))
                if int(i)>=int(startdate) and int(i)<=int(enddate):
                    accountmoney=self.accountmoney(i,account_df,cashinhand)
                    moneyrecord_df.loc[i,'money']=accountmoney  

        #moneyrecord_df.plot()       
        #print(moneyrecord_df)
        #print (total_portfolio)
        #print(moneyrecord_df)
        #moneyrecord_df.to_csv('1224-9-9tingban.csv')
        print("Final profit my portfolio:")
        print((moneyrecord_df.loc[int(enddate)]['money']-cash)/cash)    
        return (moneyrecord_df)
        
#构建函数跟踪benchmark的资产变化，初始时若无数据就不买，若出现新的基金就进行调仓，永远保证仓里是现有所有基金等权重
    def benchtest(self,startdate,cash,enddate):
        
        moneyrecord_df=pd.DataFrame()
        #建立记录所需list和日期
        shangzhe_daterecord=self.datetransfer(self.datecal(startdate,0))
        shangzhe_coderecord=[]
        xiazhe_daterecord=self.datetransfer(self.datecal(startdate,0))
        xiazhe_coderecord=[]
        #初始化cashinhand
        cashinhand=cash
        #建立account_df初始状态
        account_df=pd.DataFrame()     
        for i in df_B_close.columns:
            account_df.loc[str(int(i)),'hand']=0
            
        numbercount=0
        start=self.datetransfer(startdate)
        #在日期里面做循环
        for i in date_ls:            
            #第一天首先买入现存所有
            #print(float(i))
            #print(float(self.datetransfer(startdate)))
            if float(i)==float(self.datetransfer(startdate)):   
                #print("11111111111111111111111111111111111111111111111111111111111")
                for j in df_B_close.columns:
                    price=df_B_close.loc[i][j]
                    if price!=0:
                        numbercount+=1
                cash_buy=cashinhand
                #print(numbercount)
                for j in df_B_close.columns:
                    price=df_B_close.loc[i][j]
                    if price!=0:
                        print(j)
                        #print(account_df)
                        account_df=self.buy(int(j),i,account_df,cash_buy,numbercount)
                        cashinhand=self.buyloss(cashinhand,cash_buy,numbercount)
                #print(account_df)
            
            #非第一天判断
            elif float(i)>float(self.datetransfer(startdate)):
                #对每一天各个记录的list进行计数            
                count_shangzhe=0
                count_xiazhe=0
                for s in shangzhe_coderecord:
                    count_shangzhe+=1
                for s in xiazhe_coderecord:
                    count_xiazhe+=1
                #每天先进行一个判断，今天是否已经到了持仓的基金上折返现或者下折手数变化的日期，之所以先判断这个是为了防止有的基金在上折之后停盘日被选择卖出，这样可以先回收利润，然后再卖出，如果下折可以先修改手数，然后卖出，符合实际
                if i==int(shangzhe_daterecord):
                    #print(i)
                    #print("premium")
                    #print(cashinhand)
                    datebefore=self.tradedatecal(shangzhe_daterecord,-3,date_ls_total)
                    #print(datebefore)
                    #print(type(datebefore))
                    for s in shangzhe_coderecord:
                        navB1=float(df_B_nav.loc[int(datebefore)][int(s)])
                        navB2=float(df_B_nav.loc[int(shangzhe_daterecord)][int(s)])
                        cashinhand+=(float(navB1)-float(navB2))*account_df.loc[str(s)]['hand']
                    shangzhe_coderecord=[]
                if i==int(xiazhe_daterecord):
                    #print(i)
                    #print("discount")
                    #print(cashinhand)
                    datebefore=self.tradedatecal(xiazhe_daterecord,-3,date_ls_total)
                    for s in xiazhe_coderecord:
                        navB1=float(df_B_nav.loc[int(datebefore)][int(s)])
                        navB2=float(df_B_nav.loc[int(xiazhe_daterecord)][int(s)])
                        account_df.loc[str(s)]['hand']=account_df.loc[str(s)]['hand']*float(navB1)/navB2
                    xiazhe_coderecord=[]
                #然后再开始测试和买卖
                numberadd=0
                for j in df_B_close.columns:
                    onedaybefore=self.tradedatecal(i,-1,date_ls_total)
                    price_1=df_B_close.loc[int(onedaybefore)][j]
                    price=df_B_close.loc[int(i)][j]
                    
                    if price_1==0 and price!=0:
                        numbercount+=1
                        numberadd+=1
                if numberadd!=0:
                    #print(account_df)
                    for k in account_df.index:
                        if account_df.loc[k]['hand']!=0:
                            #写一个sellgain函数计算每次卖出cashinhand的变化结果
                            cashinhand=self.sellgain(int(k),i,account_df,cashinhand)
                            account_df=self.sell(int(k),account_df)
                    #再买入
                    cash_buy=cashinhand
                    #print(cash_buy)
                    for j in df_B_close.columns:
                        price=df_B_close.loc[int(i)][j]
                        if price!=0:
                            account_df=self.buy(int(j),i,account_df,cash_buy,numbercount)
                            cashinhand=self.buyloss(cashinhand,cash_buy,numbercount)
            
                for k in account_df.index:
                    if account_df.loc[k]['hand']!=0 and self.shangzhedate(k,i,date_ls_total)==1:
                        #print("shangzhe")
                        #print(i)
                        #print(type(i))
                        #print(k)
                        shangzhe_daterecord=self.tradedatecal(i,2,date_ls_total)
                        #print(shangzhe_daterecord)
                        shangzhe_coderecord.append(k)
                    if account_df.loc[k]['hand']!=0 and self.xiazhedate(k,i,date_ls_total)==1:
                        #print("xiazhe")
                        #print(i)
                        #print(k)
                        xiazhe_daterecord=self.tradedatecal(i,2,date_ls_total)
                        xiazhe_coderecord.append(k)
                        
            #记录每日总资产
            #print(cashinhand)
                        
            if int(i)>=int(start) and int(i)<=int(enddate):
                accountmoney=self.accountmoney(i,account_df,cashinhand)
                moneyrecord_df.loc[i,'moneybenchmark']=accountmoney
            
        print("Final profit benchmark:")
        print((moneyrecord_df.loc[int(enddate)]['moneybenchmark']-cash)/cash)   
        moneyrecord_df.to_csv("Benchmark_B.csv")
        return (moneyrecord_df)

#绘制对比图
    def plot_contrast(self,moneyrecord1,moneyrecord2,date_ls,startdate,enddate):
        startdate=self.datetransfer(startdate)
        date_ls_change=[]
        for i in date_ls:
            if int(i)>=int(startdate) and int(i)<=int(enddate):
                date_ls_change.append(i)
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
        monthsFmt = DateFormatter("%b '%y")
        print(date_ls_change)
        #print(date_ls)
        date = [str(e) for e in date_ls_change]
        date_ls = [datetime.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv=moneyrecord1['money'].tolist()
        print(algo_pv)
        bench_pv=moneyrecord2['moneybenchmark'].tolist()
        fig, ax = plt.subplots()
        plt.gca().set_color_cycle(['blue', 'red'])
        ax.plot_date(date_ls, algo_pv,'-')
        ax.plot_date(date_ls, bench_pv,'-')
        months.MAXTICKS=5000
        mondays.MAXTICKS=5000
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('P&L')
        plt.legend(['strategy', 'benchmark'], loc='upper left')
        plt.show()

#绘制alpha图
    def plot_alpha(self,alpha,date_ls,startdate,enddate):
        startdate=self.datetransfer(startdate)
        date_ls_change=[]
        for i in date_ls:
            if int(i)>=int(startdate) and int(i)<=int(enddate):
                date_ls_change.append(i)
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=3)
        monthsFmt = DateFormatter("%b '%y")
        #print(date_ls)
        date = [str(e) for e in date_ls_change]
        date_ls = [datetime.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv=alpha['alpha'].tolist()
        #print(algo_pv)
        fig, ax = plt.subplots()
        plt.gca().set_color_cycle(['blue', 'red'])
        ax.plot_date(date_ls, algo_pv,'-')
        months.MAXTICKS=5000
        mondays.MAXTICKS=5000
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Alpha')
        plt.legend(['alpha'], loc='upper left')
        plt.show()                            
                    
        


#KJ_profit_df=pd.DataFrame(columns=[i/10 for i in range(1,121)])
#for K in list_K:
    #for J in list_J:
        #KJ=B(cash,account,startdate,enddate,K,J)
        #KJ_total_portfolio=KJ.test(startdate,enddate,K,J,cash)
        #KJ_profit_df.loc[10*J-1,K]=KJ_total_portfolio

#KJ_profit_df.to_csv('KJ_finalprofit.csv')     