# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:18:05 2016

@author: Liu
"""
import numpy as np
import pandas as pd
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MONDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from backtestA import leverageA

class show(leverageA):
    def __init__(self,algo1,algo2):
        self.algo1=algo1
        self.algo2=algo2
        self.start=algo1.start
        self.end=algo1.end
        self.date_ls=algo1.date_ls        
        self.algo1_portfolio=algo1.portfolioValue
        self.algo2_portfolio=algo2.portfolioValue


    def plot_pl(self):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")

        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv = np.array(self.algo1_portfolio)
        bench_pv = np.array(self.algo2_portfolio)
        fig, ax = plt.subplots()
        plt.gca().set_color_cycle(['blue', 'red'])
        ax.plot_date(date_ls, algo_pv,'-')
        ax.plot_date(date_ls, bench_pv,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('P&L')
        plt.legend(['strategy', 'benchmark'], loc='upper left')
        plt.show()
       
    def plot1_pl(self,algo):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")

        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv = np.array(algo.portfolioValue)
   
        fig, ax = plt.subplots()

        ax.plot_date(date_ls, algo_pv,'-')

        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Strategy P&L')
        plt.show() 

    def plot2_pl(self,p):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")

        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv = np.array(p)
        fig, ax = plt.subplots()
        ax.plot_date(date_ls, algo_pv,'-')

        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Strategy P&L')
        plt.show()    
        
    def plot3_pl(self,p,pa,pb):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")

        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        algo_pv = np.array(p)
        algoA_pv = np.array(pa)
        algoB_pv = np.array(pb)
        fig, ax = plt.subplots()
        plt.gca().set_color_cycle(['blue', 'red','green'])
        ax.plot_date(date_ls, algo_pv,'-')
        ax.plot_date(date_ls, algoA_pv,'-')
        ax.plot_date(date_ls, algoB_pv,'-')

        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Strategy P&L')
        plt.legend(['combined', 'A','B'], loc='upper left')
        plt.show()    
        
    def plot_num(self,algo):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")
        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        num = np.array(algo.positionNum)
        fig, ax = plt.subplots()
        ax.plot_date(date_ls, num,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Stock Position Number')
        plt.show()
        
    def plot_up(self,algo):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")
        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        num = np.array(algo.up)
        fig, ax = plt.subplots()
        ax.plot_date(date_ls, num,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Up')
        plt.show()
        
    def plot_down(self,algo):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")
        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        num = np.array(algo.down)
        fig, ax = plt.subplots()
        ax.plot_date(date_ls, num,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Down')
        plt.show()
    def plot_cash(self,algo):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")
        date = [str(e) for e in self.date_ls]
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        num = np.array(algo.cashValue)
        fig, ax = plt.subplots()
        ax.plot_date(date_ls, num,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('Cash')
        plt.show()
        
    def plot_alpha(self):
        date1=dt.datetime.strptime(self.start,'%Y%m%d').date()
        date2=dt.datetime.strptime(self.end,'%Y%m%d').date()
        mondays = WeekdayLocator(MONDAY)
        months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
        monthsFmt = DateFormatter("%d %b'%y")
        date = [str(e) for e in self.date_ls]
        
        
        date_ls = [dt.datetime.strptime(d,'%Y%m%d').date() for d in date]
        
        alpha=np.array(self.algo1_portfolio)-np.array(self.algo2_portfolio)
        
        fig, ax = plt.subplots()
        ax.plot_date(date_ls,alpha,'-')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(monthsFmt)
        ax.xaxis.set_minor_locator(mondays)
        ax.autoscale_view()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.title('alpha')
        plt.show()
        
    def annualised_sharpe(self,returns, N=244):
        return np.sqrt(N) * returns.mean() / returns.std()
        
        
    def portfolio_sharpe(self,algo):
        df_portfolio=pd.DataFrame(index=self.date_ls)
        df_portfolio['strategy']=algo.portfolioValue
        df_portfolio['daily_ret'] = df_portfolio['strategy'].pct_change()
        df_portfolio['daily_excess_ret'] = df_portfolio['daily_ret'] - 0.01/244
        return self.annualised_sharpe(df_portfolio['daily_excess_ret'])
        
        
    def max_drawdown(self,algo):
        pv=algo.portfolioValue
        max_ddown=0
        max_value=pv[0]
        for i in range(len(pv)):
            drawdown=1-pv[i]/max_value
            if pv[i]>max_value:
                max_value=pv[i]
            if drawdown>max_ddown:
                max_ddown = drawdown
        return max_ddown
        
        
    def ratio(self):
        df=pd.DataFrame(columns=['Sharpe ratio','Max drawdown'])
        sharpe1=self.portfolio_sharpe(self.algo1)
        sharpe2=self.portfolio_sharpe(self.algo2)
        down1=self.max_drawdown(self.algo1)
        down2=self.max_drawdown(self.algo2)
        df['Sharpe ratio']=[sharpe1,sharpe2]
        df['Max drawdown']=[down1,down2]
        return df
        