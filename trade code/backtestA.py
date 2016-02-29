# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import operator
from tools import * 
from fv_a import delta_p,irr_mean,func2

class leverageA(object):
    def __init__(self,df_nav,df_b,df_closeA,df_openA,df_interest,df_m,df_volume,df_closeB,df_discount_ratio,
                 start='20160104',end='20160225',capital_base=1000000):
        
        self.outlier=['150022','150008','150319','150333','150351','150353','150285',\
                      '150349','150239','150253','150357','150313']


        self.universe =list(df_nav.columns.values)[1:]  
        for stock in self.outlier:        
            self.universe.remove(stock)
        
        #初始化
        
        #读取数据，A的净值和价格，B的净值
    
        #调整数据
        self.start=start   #策略起止日期
        self.end=end
        self.freq=1        #每隔1天进行仓位调整
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
        self.df_discount_ratio=df_discount_ratio.set_index(['PRICE.DATE'])
        #设置日期，记录今天和昨天日期
        self.date=start
        self.yesterday=self.date
        self.current_date=self.date
        #设置其他变量
        self.down_stock=[]#上折股票
        self.up_stock=[]#下折股票
        self.amount={}#每种分级A的数量
        #default value
        self.percent_volume=0.2
        self.percent_fva=0.2
        self.percent_irr=0.2
        self.percent_volume_t=0.01
        #设置账户信息
        self.cash_= capital_base #账户里现金
        #用于信息展示，每天的数据append到list里面，最后直接画出就ok
        self.portfolioValue=[]
        self.cashValue=[]
        self.positionNum=[]
        self.up=[]
        self.down=[]
        #设置佣金和申购赎回费率
        self.commision_redemp= 0.005 #赎回费用
        self.commision = 0.0005 #交易手续费
        self.benchmark=1
        
    def set_parameter(self,volume_p,irr_p,volume_tconstrain_p=0.1):
        self.percent_volume=volume_p #设置volume rank的百分比
        self.percent_irr=irr_p #设置 irr rank的百分比
        self.percent_volume_t=volume_tconstrain_p #如果某一天的计算下单量大于当天的成交量的10%只能按照成交量的10%交易
        #这个设置是符合现实的，因为不能过多的下单交易，大单会影响交易价格
    
#计算隐含回报率，并且排名
    def sort_by_irr(self,stocklist,date,percentage):
        irr={}
        stock_ls=[]
        #选股时不考虑下折的分级A（不能买入），只有当其净值不为1时才考虑，全部按照永续计算。
        #基于昨天的收盘价得出的隐含收益率
        for stock in stocklist:
            if self.df_closeA.loc[int(date)][stock]:
                #if self.df.loc[int(self.yesterday)][stock]!=1.00:    
                    #p = self.referencePrice[stock]
                p=self.df_closeA.loc[int(date)][stock]
                interest = self.df_interestA.loc[int(date)][stock]
                nav = self.df.loc[int(date)][stock]
                irr[stock] = interest/(p-(nav-1))
            else:
                continue
            sorted_irr = sorted(irr.items(), key=operator.itemgetter(1),reverse=True)[:int(len(irr)*percentage)]
            
            for key in sorted_irr:
                stock_ls.append(key[0])
        #print len(irr)
        return stock_ls
 
    def sort_by_fva(self,stocklist,date,percentage):
        universe2=self.sort_by_volume(self.universe,date,self.percent_volume,1)
        irr=irr_mean(universe2,date)
        delta={}
        stock_ls=[]
        #universe2=self.sort_by_volume(self.universe,0.3,1)
        for stock in stocklist:
            try:
                m=delta_p(stock,int(date),irr)
                #print stock,m
                if m>0:
                    delta[stock]=m
            except:
                continue
                #print stock,delta[stock]
        sorted_delta = sorted(delta.items(), key=operator.itemgetter(1),reverse=True)[:int(len(delta)*percentage)]
        
        for key in sorted_delta:
            stock_ls.append(key[0])
 
        return stock_ls
    
    def sort_by_downprob(self,stocklist,date,percentage):
        stock_ls=[]
        for stock in stocklist:
            navB= self.df_b.loc[int(date)][stock]
            p = func2(navB,0.05395854,  0.04635607, -0.19116219)
            if p>percentage:
                stock_ls.append(stock)
        #print stock_ls
        return stock_ls
                    
    def weight(self,stocklist,date):
        volume_sum=0
        w=[]
        stock_ls=[]
        for stock in stocklist:
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
    
    '''
    def weight(self,stocklist,date):
        w=[]
        stock_ls=[]
        for stock in stocklist:
            if self.df.loc[int(date)][stock]:
                stock_ls.append(stock)
        for stock in stock_ls:
            w.append(0.95/len(stocklist))
        return w
    '''
                
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
            
    #用于集合计算的几个函数        
    
    
    def strategy(self,date):          
        if self.benchmark==0:
            sum_discount=0
            stock_ls=[]
            stock_ls_B=[]
            stock_ls_3=[]
            for i,stock in enumerate(self.universe):
                if self.df.loc[int(self.date)][stock] and self.df_closeA.loc[int(self.date)][stock]:
                    sum_discount+=self.df_discount_ratio.loc[int(self.date)][stock]
                    stock_ls.append(stock)
                    stock_ls_B.append(self.universe[i])
            navb = 1 - self.percentage_lower_navb(stock_ls_B,date,0.6)

            if navb < 1:
                #print 1,date
                stock_ls=self.sort_by_fva(stock_ls,self.yesterday,self.percent_fva)
                            
            elif 1 <= navb :
                #print 2,date
                stock_ls=self.sort_by_irr(stock_ls,self.yesterday,self.percent_irr)
                
            #stock_ls=[x for x in stock_ls if self.df_discount_ratio.loc[int(self.yesterday)][x]<0.05]
            stock_ls=[x for x in stock_ls if self.df_closeA.loc[int(self.yesterday)][x]<1.1*self.df.loc[int(self.yesterday)][x]/((self.df_interestA.loc[int(self.yesterday)][x]+100)/100)]

            #for x in stock_ls:
                #print self.df.loc[int(self.yesterday)][x]/self.df_interestA.loc[int(self.yesterday)][x]
        if self.benchmark==2:
            stock_ls=[]
            stock_ls_1=[]
            stock_ls_2=[]
            stock_ls_3=[]
            for stock in self.universe:
                if self.df.loc[int(self.date)][stock] and self.df_closeA.loc[int(self.date)][stock]:
                    stock_ls.append(stock)
            for stock in stock_ls:
                if self.df_b.loc[int(self.yesterday)][stock]<0.8:
                    #print 1
                    stock_ls_1.append(stock)
                if 0.8<=self.df_b.loc[int(self.yesterday)][stock]<1.3:
                    #print 2                        
                    stock_ls_2.append(stock)
                if self.df_b.loc[int(self.yesterday)][stock]>=1.3:
                    if self.df_discount_ratio.loc[int(self.yesterday)][stock]<0.01:
                        #print 3
                        stock_ls_3.append(stock)
                
            a=self.sort_by_fva(stock_ls_1,self.yesterday,self.percent_fva)    
            b=self.sort_by_irr(stock_ls_2,self.yesterday,self.percent_irr) 
            #c=self.sort_by_irr(stock_ls_3,self.yesterday,self.percent_irr)
            stock_ls=union(union(a,b))

        if self.benchmark==3:   
            stock_ls=[]
            for i,stock in enumerate(self.universe):
                if self.df.loc[int(self.date)][stock] and self.df_closeA.loc[int(self.date)][stock]:
                    stock_ls.append(stock)  
            stock_ls=self.sort_by_irr(stock_ls,self.yesterday,self.percent_irr)
           
                        
        if self.benchmark==1:
            stock_ls=[]
            for stock in self.universe:
                if self.df.loc[int(self.date)][stock] and self.df_closeA.loc[int(self.date)][stock]:
                    stock_ls.append(stock)
        return stock_ls
        
    #回测主函数       
    def backtest(self,benchmark):
        self.benchmark=benchmark
        self.date_ls=daterange(self.date_ls,self.start,self.end)
        if self.benchmark==0:
            f=open('transaction_record1.txt','w')
            g=open('test1.csv','w')

        for date in self.date_ls[::self.freq]:
            print date
            self.current_date=date          
            self.yesterday=self.date
            self.date = self.current_date
            stock_ls=self.strategy(date)
            
                
            
            up_remove=[]
            down_remove=[]
            up_=0
            down_=0
            stock_to_sell=[]
            stock_to_rebalance=[]
            stock_to_add=stock_ls
            if self.amount:#记录我们portfolio有的股票，字典格式，key是股票的名字          
                stock_to_sell=diff(self.amount.keys(),stock_ls)
                stock_to_rebalance=intersects(self.amount.keys(),stock_ls)
                stock_to_add=diff(stock_ls,self.amount.keys())
                #print diff(self.union(stock_to_add,stock_to_rebalance),stock_ls)
                portfolio=self.cash_
                for stock in self.amount.keys():
                    portfolio+=self.amount[stock]*self.df_closeA.loc[int(self.date)][stock]
                    #print stock,self.amount[stock],self.df_closeA.loc[int(self.date)][stock],self.amount[stock]*self.df_closeA.loc[int(self.date)][stock]
                #print self.date,self.cash_,portfolio  
                for stock in self.amount.keys():
                    if self.df.loc[int(self.date)][stock]<self.df.loc[int(self.yesterday)][stock]:
                        
                        if self.df_b.loc[int(self.yesterday)][stock]<0.3:
                            #print 'down',stock
                            if self.df_closeB.loc[int(self.date)][stock]== self.df_closeB.loc[int(self.yesterday)][stock]:#发生下折的判断
                                self.down_stock.append([stock,self.yesterday,self.date])
                                down_+=1
                            else:
                                self.down_stock.append([stock,self.date,self.date])
                                down_+=1#记录已有投资组合里下折的股票
                                #print 'down',stock,self.date
              
                        else:
                            if stock not in [x[0] for x in self.up_stock ] and stock not in [x[0] for x in self.down_stock ] :
                                #print 'up',stock                                
                                self.up_stock.append([stock,self.date,self.yesterday])
                                up_+=1
                                #print 'up',stock,self.date
                                #print self.up_stock
                #假设全部可以赎回                
                #因为按照净值判断上下折，所以会有连续几天净值都为1，这时如果净值一旦不为1，就说明已经可以继续交易分级A，因折算造成的停盘结束，此时从记录器中移除上下折股票        
                if self.up_stock:        
                    #print self.date,self.up_stock
                    for i,up_stock in enumerate(self.up_stock):
                        if self.date_ls.index(self.date)-self.date_ls.index(self.up_stock[i][1])>1:
                            #print "zhesuan",up_stock,self.date,(self.df.loc[int(self.up_stock[i][2])][self.up_stock[i][0]]-1),self.amount.get(self.up_stock[i][0],0),+(self.df.loc[int(self.up_stock[i][2])][self.up_stock[i][0]]-1) \
                            #*self.amount.get(self.up_stock[i][0],0)
                            self.cash_ = self.cash_\
                            +(self.df.loc[int(self.up_stock[i][2])][self.up_stock[i][0]]-1) \
                            *self.amount.get(self.up_stock[i][0],0)*self.df_m.loc[int(self.date)][self.up_stock[i][0]]*(1-self.commision_redemp)
                            up_remove.append(up_stock)
                            if self.df.loc[int(self.up_stock[i][2])][self.up_stock[i][0]]-1+self.df_openA.loc[int(self.date)][self.up_stock[i][0]]<self.df_closeA.loc[int(self.up_stock[i][1])][self.up_stock[i][0]]-0.2:
                                stock_to_sell=diff(stock_to_sell,self.up_stock[i][0])#avoid irraional behavior
                    if up_remove:
                        self.up_stock=[x for x in self.up_stock if x not in up_remove]
                    stock_to_sell=diff(stock_to_sell,[i[0] for i in self.up_stock])
                    if stock_to_rebalance: 
                        stock_to_rebalance=diff(stock_to_rebalance,[i[0] for i in self.up_stock])
  
                    
                if self.down_stock:
                    for i,down_stock in enumerate(self.down_stock):
                        if self.date_ls.index(self.date)-self.date_ls.index(self.down_stock[i][1])>1:
                            self.cash_ = self.cash_+(self.df.loc[int(self.down_stock[i][2])][self.down_stock[i][0]]-0.25)*\
                            self.amount.get(self.down_stock[i][0],0)\
                            *self.df_m.loc[int(self.date)][self.down_stock[i][0]]*(1-self.commision_redemp)#下折后调整现金
                            self.amount[self.down_stock[i][0]]=0.25*self.amount.get(self.down_stock[i][0],0)
                            down_remove.append(down_stock)
                        #if self.date_ls.index(self.date)-self.date_ls.index(self.down_stock[i][1])<2:
                            #up_down-=1
                    if down_remove:
                        self.down_stock=[x for x in self.down_stock if x not in down_remove]
                    stock_to_sell=diff(stock_to_sell,[i[0] for i in self.down_stock])
                    if stock_to_rebalance: 
                        stock_to_rebalance=diff(stock_to_rebalance,[i[0] for i in self.up_stock])
                        
      
                if stock_to_sell:
                    for stock in stock_to_sell:
        
                        if self.amount[stock] > self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]:
                            #print -1,stock,self.amount[stock],int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]),self.date
                            amount = int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock])
                        else:
                            amount = self.amount[stock]
                        self.cash_+=amount*self.df_openA.loc[int(self.date)][stock]*(1-self.commision)
                        self.amount[stock]-=amount
                        if self.benchmark==0:
                            f.write(str(date))
                            f.write(", ")
                            f.write(str(stock))
                            f.write(", ")
                            f.write("sell all")
                            f.write(", ")
                            f.write(str(amount))
                            f.write("\n")
               
            
            for stock in stock_ls:
                p = self.df_openA.loc[int(self.date)][stock]
                if np.isnan(p):
                    stock_ls.remove(stock)
                if self.df.loc[int(self.date)][stock]==1.0:
                    stock_ls.remove(stock)
                    
            #买入stock_ls包含的股票
            if stock_ls:
                w= self.weight(stock_ls,self.yesterday)
                
                portfolio=self.cash_
                for stock in self.amount.keys():
                    portfolio+=self.amount[stock]*self.df_openA.loc[int(self.date)][stock]
                
                
                stock_to_buy=[]

                for i,stock in enumerate(stock_ls):
                    p = self.df_openA.loc[int(self.date)][stock]
                    amount = int(portfolio * w[i] / p)
                    if stock in stock_to_rebalance:
                        #print stock,'to rebalance'
                        change = amount-self.amount[stock]
                        if abs(change)>self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]:
                            #if change<0:
                                #print -2,stock,change,int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]),self.date
                            change = int(sign(change)*self.percent_volume_t* self.df_volume.loc[int(self.date)][stock])
                        if change>0:
                            stock_to_buy.append(stock)
                        if change<0:
                            self.cash_+=-change*p*(1+self.commision)
                            self.amount[stock]-=-change
                            if self.benchmark==0:
                                f.write(str(date))
                                f.write(", ")
                                f.write(str(stock))
                                f.write(", ")
                                f.write("sell in balance")
                                f.write(", ")
                                f.write(str(-change))
                                f.write("\n")
                        
                cash=self.cash_
                stock_to_buy_in_balance=union(stock_to_buy,stock_to_add)
                if stock_to_buy_in_balance:
                    w2=self.weight(stock_to_buy_in_balance,self.yesterday)
                    
                    for i,stock in enumerate(stock_to_buy_in_balance):
                        p = self.df_openA.loc[int(self.date)][stock]
                        amount = int(cash * w2[i] / p)
                        if self.amount.get(stock,0):
                            if abs(amount)>self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]:
                                #print 2,stock,abs(amount),int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]),self.date
                                amount=int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock])
                            self.cash_-=amount*p*(1+self.commision)
                            self.amount[stock]+=amount
                            if self.benchmark==0:
                                f.write(str(date))
                                f.write(", ")
                                f.write(str(stock))
                                f.write(", ")
                                f.write("buy in balance")
                                f.write(", ")
                                f.write(str(amount))
                                f.write("\n")
                        else:
                            if abs(amount)>self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]:
                                #print 1,stock,abs(amount),int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock]),self.date
                                amount = int(self.percent_volume_t* self.df_volume.loc[int(self.date)][stock])
                            self.cash_-=amount*p*(1+self.commision)
                            self.amount[stock]=amount
                            if self.benchmark==0:
                                f.write(str(date))
                                f.write(", ")
                                f.write(str(stock))
                                f.write(", ")
                                f.write("buy new")
                                f.write(", ")
                                f.write(str(amount))
                                f.write("\n")
                            #print stock,date
                            '''
                            判断当天买入的新股票当天是否会发生下折
                            '''
                            if self.df.loc[int(self.date)][stock]<self.df.loc[int(self.yesterday)][stock]:
                        
                                if self.df_b.loc[int(self.yesterday)][stock]<0.3:
                                    if self.df_closeB.loc[int(self.date)][stock]== self.df_closeB.loc[int(self.yesterday)][stock]:#发生下折的判断
                                        self.down_stock.append([stock,self.yesterday,self.date])
                                        down_+=1
                                    else:
                                        self.down_stock.append([stock,self.date,self.date])
                                        down_+=1#记录已有投资组合里下折的股票
                                  
                                else:
                                    if stock not in [x[0] for x in self.up_stock ] and stock not in [x[0] for x in self.down_stock ] :
                                        self.up_stock.append([stock,self.date,self.date])
                                        up_+=1
            for stock in self.amount.keys():
                if self.amount[stock]==0:                        
                        del self.amount[stock]


            #print date,"buy",stock_ls,"cash",self.cash_,len(self.amount.keys()), self.amount
            portfolio=self.cash_
            if self.benchmark==0:
                f.write("position")
                f.write(" , ")
            for stock in self.amount.keys():
                portfolio+=self.amount[stock]*self.df_closeA.loc[int(self.date)][stock]
                if self.benchmark==0:
                    f.write(str(stock))
                    f.write(" , ")
                    f.write(str(self.amount[stock]))
                    f.write(" , ")
                    f.write(str(self.amount[stock]*self.df_closeA.loc[int(self.date)][stock]))
                    f.write(" , ")
                    f.write(str(self.amount[stock]*(self.df_closeA.loc[int(self.date)][stock]-self.df_openA.loc[int(self.date)][stock])))
                    f.write("\n")
            #print date,self.amount,portfolio
            #print portfolio
            if self.benchmark==0:
                f.write("portfolio value")
                f.write(str(portfolio))
                f.write("\n")
                f.write("cash value")
                f.write(str(self.cash_))
                f.write("\n")
            self.portfolioValue.append(portfolio)
            self.cashValue.append(self.cash_)
            self.positionNum.append(len(self.amount.keys()))
            self.up.append(up_)
            self.down.append(down_)
            if self.benchmark==0:
                f.write("\n")
        if self.benchmark==0:        
            f.close()
            g.close()
            

            

        

