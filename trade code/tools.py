# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:55:02 2016

@author: Liu
"""


def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersects(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a,b):
    """ return the union of two lists """
    return list(set(a) | set(b))
 
def diff(a,b):
    a1=set(a)
    b1=set(b)
    return list(a1.difference(b1))

#在数据集里面取出根据用户定义的日期区间（我们的数据集是从2014年初到2015年11月初）
def daterange(date_ls,start,end):
    s_index=date_ls.index(int(start))
    e_index=date_ls.index(int(end))
    
    return date_ls[s_index:e_index]
#求符号
def sign(a):
    if a>0:
        return 1
    if a<0:
        return -1
    if a==0:
        return 0