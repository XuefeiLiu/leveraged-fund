'''
stock_ls selection should delete stockls that would 发生上下折

'''
import numpy as np
import pandas as pd
import operator
import datetime
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from fv_a import delta_p,irr_mean

class stock_selection(object):
    def __init__(self,df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB):

        self.outlier=['150022','150008','150319','150333','150351','150353','150285',\
                    '150349','150239','150253','150357','150313']

        self.universe =list(df_nav.columns.values)[1:]  
        for stock in self.outlier:        
            self.universe.remove(stock)
        self.date_ls = df_nav["PRICE.DATE"].tolist()    #生成交易日
        #把日期确定为index
        self.df=df_nav.set_index(['PRICE.DATE'])
        self.df_b=df_b.set_index(['PRICE.DATE'])
        self.df_closeA=df_closeA.set_index(['PRICE.DATE'])
        self.df_openA=df_openA.set_index(['PRICE.DATE'])
        self.df_interestA=df_interest.set_index(['PRICE.DATE'])
        self.df_m=df_m.set_index(['PRICE.DATE'])
        self.df_volume=df_volume.set_index(['PRICE.DATE'])
        self.df_closeB=df_closeB.set_index(['PRICE.DATE'])

        self.date = (datetime.datetime.now()).strftime("%Y%m%d") 
        self.yesterday =  (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y%m%d") 
        
        self.percent_volume=0.2
        self.percent_fva=0.1
        self.percent_irr=0.1
        self.up_stock=[]
        self.down_stock=[]
        #计算隐含回报率，并且排名
    def sort_by_irr(self,stocklist,date,percentage):
        irr={}
        #选股时不考虑下折的分级A（不能买入），只有当其净值不为1时才考虑，全部按照永续计算。
        #基于昨天的收盘价得出的隐含收益率
        for stock in stocklist:
            if self.df_closeA.loc[int(date)][stock]:
                #if self.df.loc[int(self.yesterday)][stock]!=1.00:    
                    #p = self.referencePrice[stock]
                p=self.df_closeA.loc[int(date)][stock]
                interest = self.df_interestA.loc[int(date)][stock]
                nav = self.df.loc[int(date)][stock]
                #print stock,date,type(nav),type(interest),type(p)
                irr[stock] = interest/(p-(nav-1.0))
            else:
                continue
            sorted_irr = sorted(irr.items(), key=operator.itemgetter(1),reverse=True)[:int(len(irr)*percentage)]
            stock_ls=[]
            for key in sorted_irr:
                stock_ls.append(key[0])
        #print len(irr)
        return stock_ls
 
    def sort_by_fva(self,stocklist,date,percentage):
        universe2=self.sort_by_volume(self.universe,date,self.percent_volume,1)
        irr=irr_mean(universe2,date)
        delta={}
        #universe2=self.sort_by_volume(self.universe,0.3,1)
        for stock in stocklist:
            m=delta_p(stock,int(date),irr)
            #print stock,m
            if m>0:
                delta[stock]=m
                #print stock,delta[stock]
        sorted_delta = sorted(delta.items(), key=operator.itemgetter(1),reverse=True)[:int(len(delta)*percentage)]
        stock_ls=[]
        for key in sorted_delta:
            stock_ls.append(key[0])
        
        return stock_ls
        
    def sort_by_volume(self,stocklist,date,percentage,category):
        volume={}
        if category==1:#表示按照volume的排名比例取股
            for stock in stocklist:
                if self.df_volume.loc[int(date)][stock]:
                    volume[stock]=self.df_volume.loc[int(date)][stock]
            sorted_volume = sorted(volume.items(),key=operator.itemgetter(1),reverse=True)[:int(len(volume)*percentage)]
            volume_ls=[]
            for key in sorted_volume:
                volume_ls.append(key[0])
            return volume_ls
        if category==0:#表示按照volume的绝对阈值进行筛选
            for stock in stocklist:
                if self.df_volume.loc[int(date)][stock]>1000000:
                    volume[stock]=self.df_volume.loc[int(date)][stock]
            sorted_volume = sorted(volume.items(),key=operator.itemgetter(1),reverse=True)
            volume_ls=[]
            for key in sorted_volume:
                volume_ls.append(key[0])
            return volume_ls
            
    def avg_navb(self,stocklist,date):
        #w=self.weight(stocklist,date)
        navb=[]
        for stock in stocklist:

            if self.df_b.loc[int(date)][stock]:
                navb1=self.df_b.loc[int(date)][stock]
                navb.append(navb1)
        #w=np.array(w)
        navb=np.array(navb)
        return navb.mean()
            
    def percentage_lower_navb(self,stocklist,date,value):
        i = 0
        j = 0
        for stock in stocklist:
            if self.df_b.loc[int(date)][stock]:
                i += 1
                if self.df_b.loc[int(date)][stock] < value:
                    j +=1
        #print j,i
        fj = float(j)
        fi = float(i)
        return fj / fi

    def strategy_selection(self):
        stock_ls=[]
        stock_ls_B=[]
        for i,stock in enumerate(self.universe):
            if self.df.loc[int(self.yesterday)][stock] and self.df_closeA.loc[int(self.yesterday)][stock]:
                stock_ls.append(stock)
                stock_ls_B.append(self.universe[i])
        #navb=self.avg_navb(stock_ls_B,date)
        navb = 1 - self.percentage_lower_navb(stock_ls_B,self.yesterday,0.7)
        #print navb
        
        if navb < 1:
            #print 1,date
            stock_ls=self.sort_by_fva(stock_ls,self.yesterday,self.percent_fva)
        #print date,stock_ls
                        
        elif 1 <= navb:
            #print 2,date
            stock_ls=self.sort_by_irr(stock_ls,self.yesterday,self.percent_irr)
                        
        #else:
            #print 3,date
                        
        return stock_ls
    '''
    def up_down(self,stocklist):
        if self.df.loc[int(self.date)][stock]<self.df.loc[int(self.yesterday)][stock]:
            if self.df_b.loc[int(self.yesterday)][stock]<0.3:
                if self.df_openB.loc[int(self.date)][stock]== self.df_closeB.loc[int(self.yesterday)][stock]:#发生下折的判断
                    self.down_stock.append([stock,self.yesterday,self.date])
                
                else:
                    self.down_stock.append([stock,self.date,self.date])
                    
              
            else:
                if stock not in [x[0] for x in self.up_stock ] and stock not in [x[0] for x in self.down_stock ] :
                    self.up_stock.append([stock,self.date,self.date])
    '''    
                  
        
    def output(self):
        stock_ls = self.strategy_selection()
        df = pd.DataFrame()
        df['stock'] = stock_ls
        s = str(self.date) + '_A_stocklist.csv'
        df.to_csv(s)
        return s
        
class rebalance(object):
    def __init__(self,df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,stock_ls):
        self.outlier=['150022','150008','150319','150333','150351','150353','150285',\
                    '150349','150239','150253','150357','150313']

        self.universe =list(df_nav.columns.values)[1:]  
        for stock in self.outlier:        
            self.universe.remove(stock)
        self.date_ls = df_nav["PRICE.DATE"].tolist()    #生成交易日
        #把日期确定为index
        self.df=df_nav.set_index(['PRICE.DATE'])
        self.df_b=df_b.set_index(['PRICE.DATE'])
        self.df_closeA=df_closeA.set_index(['PRICE.DATE'])
        self.df_openA=df_openA.set_index(['PRICE.DATE'])
        self.df_interestA=df_interest.set_index(['PRICE.DATE'])
        self.df_m=df_m.set_index(['PRICE.DATE'])
        self.df_volume=df_volume.set_index(['PRICE.DATE'])
        self.df_closeB=df_closeB.set_index(['PRICE.DATE'])

        self.date = (datetime.datetime.now()).strftime("%Y%m%d") 
        self.yesterday =  (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y%m%d") 
        #设置其他变量
        #self.down_stock=[] #上折股票
        #self.up_stock=[] #下折股票
        #self.amount=amount #每种分级A的数量
        #self.percent_volume_t=0.1
        #设置账户信息
        #self.cash_= cash #账户里现金
        #用于信息展示，每天的数据append到list里面，最后直接画出就ok
        #self.portfolioValue=[]
        #self.cashValue=[]
        #self.positionNum=[]
        #self.up=[]
        #self.down=[]
        #设置佣金和申购赎回费率
        #self.commision_redemp= 0.005 #赎回费用
        #self.commision = 0.0005 #交易手续费
        
        self.stock_ls = stock_ls
        
    def weight(self,stocklist,date):
        volume_sum=0
        w=[]
        stock_ls=[]
        for stock in stocklist:
            stock=str(stock)
            if self.df.loc[int(date)][stock]:
                stock_ls.append(stock)
                volume_sum+=self.df_volume.loc[int(date)][stock]
        for stock in stock_ls:
            w1=self.df_volume.loc[int(date)][stock]
            if float(volume_sum)!=0:
                w.append(float(w1)/float(volume_sum))
            else:
                w.append(0)
        return w
        
    def stock_amount(self):
        w = self.weight(self.stock_ls, self.yesterday)
        df = pd.DataFrame()
        df['stock'] = self.stock_ls
        df['weight'] = w        
        return df
        
    def output(self):
        df = self.stock_amount()
        close=[]
        for s in df['stock'].values:
            close.append(self.df_closeA.loc[int(self.yesterday)][str(s)])
        df['close']=close
        print df
        s = str(self.date) + '_A_target.csv'
        df.to_csv(s)
        
        return 0

def main():
    df_nav = pd.read_csv('NAVA.csv')
    df_b = pd.read_csv('NAVB.csv')
    df_closeA=pd.read_csv('closeA.csv')
    df_openA=pd.read_csv('openA.csv')
    df_interest=pd.read_csv('interestA.csv')
    df_m=pd.read_csv('mA.csv')
    df_volume=pd.read_csv('volumeA.csv')
    df_closeB=pd.read_csv('closeB.csv')

    stock = stock_selection(df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB)
    s = stock.output()
    
    stocklist = pd.read_csv(s)['stock'].tolist()
    stock2 = rebalance(df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,stocklist)
    stock2.output()
    
    
if __name__=="__main__":
    main()