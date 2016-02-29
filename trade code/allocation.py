# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 12:00:01 2016

@author: Liu
"""
import numpy as np
def sharpe(portfolioValue):
    pReturn=portfolioValue.pct_change()
    Mean=pReturn.mean()*244-0.03
    Std=pReturn.std()*np.sqrt(244)
    return Mean/Std
def date_split(date_ls,n):
    

