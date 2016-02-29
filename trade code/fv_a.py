#encoding=utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from operator import itemgetter
from scipy.optimize import curve_fit
import statsmodels.tsa.stattools as ts
fn = os.path.join(os.path.dirname(__file__), 'data')
df_closeB=pd.read_csv(fn+'/closeB.csv')
df_navB=pd.read_csv(fn+'/NAVB.csv')
df_navA=pd.read_csv(fn+'/NAVA.csv')
date_ls = df_navA["PRICE.DATE"].tolist()[:-60]
df_navA=df_navA.set_index(["PRICE.DATE"])
df_closeB=df_closeB.set_index(["PRICE.DATE"])
df_navB=df_navB.set_index(["PRICE.DATE"])

df_openA = pd.read_csv(fn+'/openA.csv')
df_openA = df_openA.set_index(["PRICE.DATE"])

df_closeA = pd.read_csv(fn+'/closeA.csv')
df_closeA = df_closeA.set_index(["PRICE.DATE"])

df_interestA = pd.read_csv(fn+'/interestA.csv')
df_interestA = df_interestA.set_index(["PRICE.DATE"])

df_NAVA = pd.read_csv(fn+'/NAVA.csv')
df_NAVA = df_NAVA.set_index(["PRICE.DATE"])

T = 50

universe =['150181','150171','150152','150227','150018','150235','150223','150117','150209','150200','150221','502011','150184','150157','150130','150194','150196','150205','150051','150177','150261','150022','150243','150123','150211','502004','150231','150192','150265','150100','150343','150219','502049','150096','150203','150329','150085','150198','150303','150299','150106','150335','150190','150186','150275','150301','150173','150291','150315','502037','150217','150241','150251','150317','502054','502007','150289','150325','150277','150295','150028','150179','150012','150281','150321','150269','150150','150213','150207','150247','150287','150229','150225','502057','150249','150059','150267','502014','150323','150255','150237','150305','150331','150259','502031','150148','150307','150245','150215','150297','150030','150283','150309','150108','150311','150273','150083','150257','150135','150090','150293','150279','150327','150104','502041','150233','150167','150008','150271','150140','150112','150057','502024','150094','150073','502021','150263','150088','502001','150076','150138','150053','150145','150121','150092','150064','502017','150055','150285','150349','150239','150253','150357','150313','502027','150319','150333','150351','150353']
universe2=['150209','150171','150181','150194','150130','150227','150152','150184','502004',
'502011','150018','150051','150221','502007','150205','150261','150277','150235',
'150303','150177']

def down(stock,today,day):
    index_today=date_ls.index(today)
    for i in xrange(day+1):

        if 0<df_navB.loc[date_ls[index_today+i]][stock]<0.25 :
            return 1
        elif 0<df_navB.loc[date_ls[index_today+1 ]][stock]>0.9 \
            and 0<df_navB.loc[date_ls[index_today]][stock]<0.3: #xi:why 1 not i ?
            return 1

        else:
            continue
    return 0


def pa_cal (NAV_A0, P_A0, pro, avg_delta_openA): 
    P_A1 = (NAV_A0 - 0.25) + 0.25 * (P_A0 + avg_delta_openA)
    pa = (1-pro) * P_A0 + pro * P_A1
    return pa
    
def irr_mean(stocklist,date):
    irr={}
    #选股时不考虑下折的分级A（不能买入），只有当其净值不为1时才考虑，全部按照永续计算。
    #基于昨天的收盘价得出的隐含收益率
    for stock in stocklist:
        if df_closeA.loc[int(date)][stock]:
            #p = self.referencePrice[stock]
            p=df_closeA.loc[int(date)][stock]
            interest = df_interestA.loc[int(date)][stock]
            nav = df_navA.loc[int(date)][stock]
            irr[stock] = interest/(p-(nav-1))
        else:
            continue

    stock_ls=[]
    for key in irr:
        stock_ls.append(irr[key])

    irr_mean = sum(stock_ls) / len(stock_ls)

    return irr_mean    

def fv_pA (stock, date, irr):

    interest = df_interestA.loc[int(date)][stock]
    nav = df_navA.loc[int(date)][stock]
    #date_days_later = date_ls[date_ls.index(date)+day]
    P_A0 = interest / irr + (nav -1)
    P_A0_days_later = interest / irr 
    P_A1 = (nav  - 0.25) * 1 + 0.25 * P_A0_days_later
    navB = float(df_navB.loc[int(date)][stock])
    
    #p = func2 (navB, 0.05578527,  0.03522539, -0.20662114) alldays
   # p = func2(navB, 0.04781738 , 0.05343965, -0.18333949) 100day
    p = func2(navB,0.05395854,  0.04635607, -0.19116219)
    return p * P_A1 + (1 - p) * P_A0    
    
def delta_p (stock, date,irr):
    return fv_pA(stock, date,irr) - df_closeA.loc[int(date)][stock]


def func(x, a, b, c, d):
    return a*np.exp(b*x) + c*np.exp(d*x)
    
def func2(x, a, b, c):
    return (a * x + b) / (x + c)
    
def fit_curve(N):
    x,y = down_prob3(N)
    X_data = np.array(x)
    Y_data = np.array(y)
    opt,cov = curve_fit (func2, X_data, Y_data)
    return opt
    

'''
def down_prob(day):
    date_down=[]
    date_day_before=[]
    stock_down=[]
    B_nav=[]
    #这一段程序是找出day天前发生下折的股票其day天前的净值的最大值和最小值，同时可记录日期等参数
    for i,date in enumerate(date_ls[:-day]):
        for stock in universe:
            if 0<df_navB.loc[date_ls[i-1]][str(int(stock[:6])+1)+stock[6:]]<0.25 and df_navB.loc[date][str(int(stock[:6])+1)+stock[6:]]>0.25:
                if df_closeB.loc[date][str(int(stock[:6])+1)+stock[6:]]== df_closeB.loc[date_ls[i+1]][str(int(stock[:6])+1)+stock[6:]]:
                    down_date=date
                elif df_closeB.loc[date][str(int(stock[:6])+1)+stock[6:]]== df_closeB.loc[date_ls[i-1]][str(int(stock[:6])+1)+stock[6:]]:
                    down_date=date_ls[i-1]
                else:
                    continue
                date_down.append(down_date)
                date_day_before.append(date_ls[date_ls.index(down_date)-day])
                stock_down.append(stock)
                B_nav.append(df_navB.loc[date_ls[date_ls.index(down_date)-day]][str(int(stock[:6])+1)+stock[6:]])

                        
                   
    min_nav=min(B_nav)
    max_nav=max(B_nav)
    N=int((max_nav-min_nav)/0.05)+1
    count={}#下折的计数
    count2={}#不下折的计数
    prob={}
    #记录下折前day天B净值的分布情况，用count计数
    #初始化为0      
    for i in xrange(N):
        count[i]=0
        count2[i]=0
    #找到day天内不下折的
    for i in xrange(N):
        for stock in universe:
            for date in date_ls[:-day]:
                if min_nav+0.05*i<=df_navB.loc[date][str(int(stock[:6])+1)+stock[6:]]<min_nav+0.05*(i+1):
                    if down(stock,date,day)==0:
                        print "is 0",i,stock,date,df_navB.loc[date][str(int(stock[:6])+1)+stock[6:]]
                        count2[i]+=1
                    if down(stock,date,day)==1:
                        count[i]+=1
                        print "is 1",i,stock,date,df_navB.loc[date][str(int(stock[:6])+1)+stock[6:]]
    for i in xrange(N):
        if count.get(i,0):
            prob[i]=float(count[i])/float(count2[i]+count[i])
        else:
            prob[i]=0
    pdf=[]

    for i in prob.keys():
        pdf.append(prob[i])
    
    
    
    r=[]
    for j in xrange(N):    
        r.append(min_nav+j*0.05)
    
    return r,pdf
    
    pdf=tuple(pdf)
    ind=np.arange(N)
    fig,ax=plt.subplots()
    ax.bar(ind,pdf)
    ax.set_ylabel('probability of down')
    ax.set_xlabel('navB')
    ax.set_title(str(day)+'days before down')
    ax.set_xticks(ind)
    ax.set_xticklabels(tuple(r))
    plt.show()
    
    
    df=pd.DataFrame()
    df['date_down']=date_down
    df['date_day_before']=date_day_before
    df['stock_down']=stock_down
    df['B_nav']=B_nav
    
    
'''
      
def down_prob2(navb):
    stock_state=[]
    count_2=[]
    count_1=[]
    for i in xrange(len(universe)):
        stock_state.append(3)
        count_2.append(0)
        count_1.append(0)
    for i,stock in enumerate(universe):
        for date in date_ls:
            if 0.25<df_navB.loc[date][stock]<=navb:
                
                if stock_state[i]==3:
                    count_2[i]+=1
                stock_state[i]=2

            if 0<df_navB.loc[date][stock]<=0.25:
                
                if stock_state[i]==2:
                    count_1[i]+=1
                    
                if stock_state[i]==3:
                    count_1[i]+=1
                    count_2[i]+=1
                stock_state[i]=1
            if df_navB.loc[date][stock]>navb:
                stock_state[i]=3

    sum_count_2=float(sum(count_2))
    sum_count_1=float(sum(count_1))
    return sum_count_1/sum_count_2
def down_prob3(N):
    X=[]
    Y=[]
    for i in xrange(N):
        x=0.251+(i+1)*0.02
        y=down_prob2(x)
        #print x,y
        X.append(x)
        Y.append(y)
    return X,Y
def main():
    #绘制一到五天内下折的概率分布
    #for i in xrange(5):
    #print fit_curve(30)
    '''
    list=[]
    stock_ls=universe2
    ls_date=date_ls[date_ls.index(int(20150107)):]
    for i in xrange(len(stock_ls)):
        list.append([])
    
    for i, stock in enumerate(stock_ls):
        for date in ls_date:
            p=delta_p (stock, date)
            if abs(p)<0.5 and 0<df_navB.loc[int(date)][stock]<1:
                print date,p
                list[i].append(p)
    for i in xrange(len(list)):
        try:
            print ts.adfuller(list[i],1)
        except:
            continue
        fig,ax=plt.subplots()
        ax.plot(list[i])
        #lt.plot(list[i])
        plt.show()


    '''
    #print func2(0.927,0.0304,  0.05573, -0.1875)
    #irr_mean(universe2,'20150911')
    #down_prob3(10)
    
if __name__=="__main__":
    main()
    
    