import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from templateplot import *

def gridYear(df,coluna,tam):
    time = np.arange(1950,2020+2*tam,tam)
    media = []
    for i,j in zip(time[:-1],time[1:]):
        media.append(df[coluna][(df['release_year']<j) & (df['release_year']>=i)].mean())
    media = np.array(media)
    time = time[:-1][~np.isnan(media)]
    media = media[~np.isnan(media)]
    return time, np.array(media)

def multipleTemporalPlot(df,coluna,titulo):
    label = np.unique(df[coluna].values)
    fig, ax = plt.subplots(1,1,figsize=(18, 9))
    plt.title(titulo, size=18)
    for u in label:
        d_ = df[df[coluna] == u]
        x,y = np.unique(d_['release_year'].values,return_counts = True)
        ax = temporalplot(ax,x,y,u)
        plt.legend()
    #plt.legend()

def loadcsv(file):
    return pd.read_csv(file)

def check(df,coluna,check):
    return df[df[coluna]==check]

def sorting(a,b):
    arr1inds = b.argsort()
    a = a[arr1inds[::-1]]
    b = b[arr1inds[::-1]]
    return a,b

def calculate(df,coluna,value,tipo):
    if(tipo=='sum'):
        df_ = df[[coluna,value]].groupby(by = coluna,as_index = False).sum()
    elif(tipo=='mean'):
        df_ = df[[coluna,value]].groupby(by = coluna,as_index = False).mean()
    elif(tipo=='median'):
        df_ = df[[coluna,value]].groupby(by = coluna,as_index = False).median()
    elif(tipo=='count'):
        df_ = df[[coluna,value]].groupby(by = coluna,as_index = False).count()
    x,y = df_[coluna].values,df_[value].values
    if(type(x[0])==str):
        x,y = sorting(x,y)
        x = np.array([i.replace(" ","\n") for i in x])
    return x.T,y.T

def groupBar(df,colunas,valores,tipos,titulo,Graphs,col = 'row'):
    
    if(type(colunas) == str):
        x,y = calculate(df,colunas,valores,tipos)
    else:
        x,y = np.array([np.array(calculate(df,coluna,value,tipo)).T for coluna,value,tipo in zip(colunas,valores,tipos)]).T
    
    x,y = x.T,y.T

    generateGraphs(x,y,titulo,Graphs,col)

def cleaningNan(df,coluna,sub):
    index = df[coluna][df[coluna].isnull()].index
    df.loc[index,coluna] = sub
    return df

def cleaningvector(df,coluna):
    g =[i.replace('[','').replace(']','').replace('\'','').split(', ') for i in df[coluna].values]
    df = df.drop(columns = [coluna])
    df[coluna] = g
    return df