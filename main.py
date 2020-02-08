import pandas as pd
import numpy as np
import os
from IPython.display import display#因为中英混合，直接print对不齐
import ast    #将字符串转换成字典的库
os.chdir("F:\\nga")
#读取各个表格
support = pd.read_excel('队友.xlsx',encoding = 'gbk')
suit = pd.read_excel('礼装.xlsx',encoding = 'gbk')
cos = pd.read_excel('衣服.xlsx',encoding = 'gbk')
ene = pd.read_excel('敌人.xlsx',encoding = 'gbk')
ene.iloc[0,3].find('男性')#在字符串中寻找字符，找到了返回下标，没找到返回-1,rfind可以从右往左找，index找不到抛出ValueError
srv = pd.read_excel('光炮从者.xlsx',encoding = 'gbk')
for i in range(0, len(srv)):
    if(type(srv.iloc[i,10]) == str):
        srv.set_value(i,'特攻',ast.literal_eval(srv.iloc[i,10]))
    if(type(srv.iloc[i,12]) == str):
        srv.set_value(i,'宝具特攻倍率',ast.literal_eval(srv.iloc[i,12]))
#技能特攻函数
def parameter_special(df1,df2,i,m):
    result = 0
    if(type(df1.iloc[i,10]) == dict):
        for key in df1.iloc[i,10].keys():#遍历这个字典的key
            if(df2.iloc[m,3].find(key) != -1):
                result = result + df1.iloc[i,10][key]
        return result
    else:
        return result
#宝具特攻函数
def parameter_npspecial(df1,df2,i,m):
    result = 1
    if(type(df1.iloc[i,12]) == dict):
        for key in df1.iloc[i,12].keys():#遍历这个字典的key
            if(df2.iloc[m,3].find(key) != -1):
                result = result * df1.iloc[i,12][key]
        return result
    else:
        return result
#计算结果函数，接收从者，队友，礼装，衣服四个表的index
def res(i,j,k,l,m):
    parameter_class = pd.read_excel('职阶克制表.xlsx',encoding = 'gbk')#左边是己方，上面是敌方
    parameter_class.index = ['S','A','L','R','C','AS','B','SH','RU','AV','MC','AL','F','B1','B2','B3']
    ren = {'tian':0.9,'di':1.1,'ren':1.0,'xing':1.0}
    di = {'tian':1.1,'di':1.0,'ren':0.9,'xing':1.0}
    tian = {'tian':1.0,'di':0.9,'ren':1.1,'xing':1.0}
    if((ene.iloc[m,2]) == 'ren'):
        parameter_camp = ren[srv.iloc[i,8]]
    if((ene.iloc[m,2]) == 'di'):
        parameter_camp = di[srv.iloc[i,8]]
    if((ene.iloc[m,2]) == 'tian'):
        parameter_camp = tian[srv.iloc[i,8]]
    res = 0.23 * 0.9 * (srv.iloc[i,1] + suit.iloc[k,1]) * srv.iloc[i,2] * srv.iloc[i,4] * (1 + srv.iloc[i,5] + support.loc[j,srv.iloc[i,3]] + suit.loc[k,srv.iloc[i,3]] + cos.loc[l,srv.iloc[i,3]]) * srv.iloc[i,6] * parameter_class.loc[srv.iloc[i,7],ene.iloc[m,1]] * parameter_camp * (1 + srv.iloc[i,9] + support.iloc[j,1] + suit.iloc[k,2] + cos.iloc[l,1]) * (1 + parameter_special(srv,ene,i,m) + srv.iloc[i,11] + support.iloc[j,5] + suit.iloc[k,6] + cos.iloc[l,5]) * parameter_npspecial(srv,ene,i,m) + support.iloc[j,6]
    return res
#i为从者数，j为队友组合数，k为礼装数，l为衣服数，m为敌人序号，j为3时不算需要换人的组合
com = pd.read_excel('组合.xlsx',encoding = 'gbk')
n = 0
m = 0
for i in range(51):
    for j in range(3):
        for k in range(7):
            for l in range(7):
                if(srv.iloc[i,13] + support.iloc[j,7] + suit.iloc[k,7] + cos.iloc[l,6] >= 1):
                    if(res(i,j,k,l,m) > 100000):
                        s1 = pd.Series([srv.iloc[i,0],support.iloc[j,0],suit.iloc[k,0],cos.iloc[l,0],res(i,j,k,l,m)],index = ['从者','队友','礼装','衣服','伤害'])
                        s1.name = n
                        com = com.append(s1)
                        n = n + 1
display(com)
com.to_excel('组合结果.xlsx')
