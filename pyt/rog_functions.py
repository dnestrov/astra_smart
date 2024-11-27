#python3 read_exps_rog.py 11293 11295
import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
orig_stdout = sys.stdout
conn = Connection('192.168.1.7:8000')
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
#shotnumber=360
MAGRUN='BEST.'
ROGnam=[
    'DIVPSRB',
    'DIVPSRT',
    'HFSPSRB',
    'HFSPSRT',
    'MCB',
    'MCT',
    'GASBFLB',
    'GASBFLT',
    'BVLB',
    'BVLT',
    'DIVB',
    'DIVT',
    'INIVC000',
    'MCWIRE',
    'DIVBWIRE',
    'BVLWIRE',
    'DIVTWIRE',
    'SOLWIRE',
    'BVUBWIRE',
    'BVUTWIRE',
    'PSHBWIRE',
    'PSHTWIRE',
    'INIVC000raw',
    'TFWIRE'
]
FONTSIZE=12
def plot_rog_exp(index,shots,newfigure):
    ni=len(index)
    ns=len(shots)
    print(ni,ns)
    if ni == 0: return
    for i in range(0,ns):
        shot=int(shots[i])
        BEST=''
        if shot > 10800:BEST=MAGRUN
        print('ST40:'+str(shot))
        conn.openTree('ST40',shot)
        TIMEmag=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()

        jj=0
        for j in index-np.array([1]):
            signame='MAG.'+BEST+'ROG.'+ROGnam[j]+':I'
            if ROGnam[j] =='INIVC000raw':
                signame='PCS.TEPCS_DATA.MEASUREMENTS.ROGOWSKI.CURRENT:INIVC000'
            print(signame)
            ROG0=conn.get(signame).data()
            if jj==0:
                ROG1=ROG0
            elif jj==1:
                ROG1=np.append([ROG1],[ROG0],axis=0)
            else:
                ROG1=np.append(ROG1,[ROG0],axis=0)
            jj=jj+1

        ROG1=ROG1/1e3#go to kA
        conn.closeTree('st40',shot)
        if newfigure: 
            plt.figure('Rogowski kA')
            plt.rc('font', size=FONTSIZE)
        for j in range(0,ni):
            if ni==1:plt.plot(TIMEmag,ROG1,label=ROGnam[index[j]-1]+'#'+str(shot))
            if ni>1:plt.plot(TIMEmag,ROG1[j],label=ROGnam[index[j]-1]+'#'+str(shot))
            #if ni==1:plt.plot(TIMEmag,ROG1,col[j],label=ROGnam[index[j]-1]+'#'+str(shot))
            #if ni>1:plt.plot(TIMEmag,ROG1[j],col[j],label=ROGnam[index[j]-1]+'#'+str(shot))

def read_rog_exp_all(shot,name,t1,t2):
    BEST=''
    if shot > 10800:BEST=MAGRUN
    print('ST40:'+str(shot))
    conn.openTree('ST40',shot)
    TIMEmag=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()
    iupa=np.where(TIMEmag > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEmag < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEmag[idw:iup]
    ROG1=np.array([])
    for j in range(0,len(name)):
        signame='MAG.'+BEST+'ROG.'+name[j]+':I'
        if name[j] =='INIVC000raw':
            signame='PCS.TEPCS_DATA.MEASUREMENTS.ROGOWSKI.CURRENT:INIVC000'
        print(signame)
        ROG=conn.get(signame).data()
        ROG0=np.mean(ROG[idw:iup])
        ROG1=np.append(ROG1,ROG0)
    ROG1=ROG1/1e3#go to kA
    conn.closeTree('st40',shot)
    return ROG1
def read_rog_exp_mean(shot,name,t1,t2):
    BEST=''
    if shot > 10800:BEST=MAGRUN
    print('ST40:'+str(shot))
    conn.openTree('ST40',shot)
    TIMEmag=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()
    iupa=np.where(TIMEmag > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEmag < t1)
    idw=idwa[0][len(idwa[0])-1]
    TIME=TIMEmag[idw:iup]
    signame='MAG.'+BEST+'ROG.'+name+':I'
    if name =='INIVC000raw':
        signame='PCS.TEPCS_DATA.MEASUREMENTS.ROGOWSKI.CURRENT:INIVC000'
    print(signame)
    ROG=conn.get(signame).data()
    ROG1=np.mean(ROG[idw:iup])
    ROG1=ROG1/1e3#go to kA
    conn.closeTree('st40',shot)
    return ROG1
def plot_ipl_rog_exp(shots):
#           1         2         3         4        5     6      7         8
#ROGnam=['DIVPSRB','DIVPSRT','HFSPSRB','HFSPSRT','MCB','MCT','GASBFLB','GASBFLT']
    index=[1,2,3,4,5,6,7,8]
    ng=len(ROGnam)
    ni=len(index)
    ns=len(shots)
    for i in range(0,ns):
        shot=int(shots[i])
        BEST=''
        if shot > 10800:BEST=MAGRUN
        print(shot)
        conn.openTree('ST40',shot)
        TIMEmag=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()
        jj=0
        for j in index-np.array([1]):
            signame='MAG.'+BEST+'ROG.'+ROGnam[j]+':I'
            print(signame)
            ROG0=conn.get(signame).data()
            if jj==0:
                ROG=ROG0
            else:
                ROG=ROG+ROG0            
            jj=jj+1

        ROG=ROG/1e3#go to kA
        j=13
        signame='MAG.'+BEST+'ROG.'+ROGnam[j-1]+':I'
        INIVC000=conn.get(signame).data()/1000
        conn.closeTree('st40',shot)
        IPL=INIVC000-ROG
        plt.figure('Rogowski kA')
        plt.rc('font', size=FONTSIZE)
        plt.plot(TIMEmag,IPL,label='IPL from Rogowski, kA #'+str(shot))

def plot_ipl_rog_raw_exp(shots):
#           1         2         3         4        5     6      7         8
#ROGnam=['DIVPSRB','DIVPSRT','HFSPSRB','HFSPSRT','MCB','MCT','GASBFLB','GASBFLT']
    index=[1,2,3,4,7,8]
    #index=[1,2,3,4,5,6,7,8]
    ng=len(ROGnam)
    ni=len(index)
    ns=len(shots)
    print(ng,ni,ns)
    for i in range(0,ns):
        shot=int(shots[i])
        BEST=''
        if shot > 10800:BEST='BEST.'
        conn.openTree('ST40',shot)
        TIMEmag=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()
        jj=0
        for j in index-np.array([1]):
            signame='MAG.'+BEST+'ROG.'+ROGnam[j]+':I'
            print(signame)
            ROG0=conn.get(signame).data()
            if jj==0:
                ROG=ROG0
            else:
                ROG=ROG+ROG0            
            jj=jj+1

        ROG=ROG/1e3#go to kA
        signame='PCS.TEPCS_DATA.MEASUREMENTS.ROGOWSKI.CURRENT:INIVC000'
        INIVC000raw=conn.get(signame).data()/1000
        conn.closeTree('st40',shot)
        IPL=INIVC000raw-ROG
        plt.figure('Rogowski kA')
        plt.rc('font', size=FONTSIZE)
        plt.plot(TIMEmag,IPL,label='IPL from Rogowski raw, kA #'+str(shot))

def plot_ipl_rog_astra(shotastra,run):
#           1         2         3         4        5     6      7         8
#ROGnam=['DIVPSRB','DIVPSRT','HFSPSRB','HFSPSRT','MCB','MCT','GASBFLB','GASBFLT']
    index=[1,2,3,4,5,6,7,8]
    ni=len(index)
    conn.openTree('astra',shotastra)
    T=conn.get(run+':TIME')
    jj=0
    for j in index-np.array([1]):
        signame=run+'.ROG.'+ROGnam[j]+':I'
        print(signame)
        ROG0=conn.get(signame)
        if jj==0:
            ROG=ROG0
        else:
            ROG=ROG+ROG0            
        jj=jj+1
    ROG=ROG/1e3#go to kA
    j=13
    signame=run+'.ROG.'+ROGnam[j-1]+':I'
    INIVC000=conn.get(signame).data()/1000
    conn.closeTree('astra',shotastra)
    IPL=INIVC000-ROG
    plt.figure('Rogowski kA')
    plt.rc('font', size=FONTSIZE)
    plt.plot(T,IPL,label='IPL from Rogowski, kA #'+str(shotastra)+'@'+run)


def plot_ipl_exp_ppfit(shotst40,t1,t2):
    conn.openTree('st40',shotst40)
    signame0='PFIT.POST_BEST.RESULTS'
    TIMEpfit=conn.get(signame0+':TIME').data()
    iupa=np.where(TIMEpfit > t2)
    iup=iupa[0][0]
    idwa=np.where(TIMEpfit < t1)
    idw=idwa[0][len(idwa[0])-1]
    plt.figure('Rogowski kA')
    plt.rc('font', size=FONTSIZE)
    IPL= conn.get(signame0+'.GLOBAL:IP').data()/1000
    plt.plot(TIMEpfit[idw:iup],IPL[idw:iup],label='IPL from PFIT POST, kA #'+str(shotst40))
    conn.closeTree('st40',shotst40)
def plot_ipl_exp_rtpfit(shotst40):
    import pcs_reading_functions as pcs
    treename='tepcs'
    RUN=''
    channel_ip_act=pcs.pcs_map32exp('IP_PFIT_ACT')
    nodename='.ACQ2106_032.CALC:'
    TIME,VAR=pcs.pcs_readsensors(shotst40,RUN,treename,channel_ip_act,'IP_PFIT_ACT',nodename)
    VAR=VAR/1000
    pcs.pcs_plot(TIME,VAR,shotst40,RUN,treename,channel_ip_act,'IP_PFIT_ACT',30)

def plot_rog_astra(index,shotastra,run):
    ni=len(index)
    if ni == 0: return
    conn.openTree('astra',shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    jj=0
    for j in index-np.array([1]):
        signame=run+'.ROG.'+ROGnam[j]+':I'
        if ROGnam[j] =='INIVC000raw':
            signame=run+'.ROG.INIVC000:I'
        print(signame)
        try:
            ROG0=conn.get(signame)
        except:
            return
        if jj==0:
            ROG1=ROG0
        elif jj==1:
            ROG1=np.append([ROG1],[ROG0],axis=0)
        else:
            ROG1=np.append(ROG1,[ROG0],axis=0)
        jj=jj+1
            
    conn.closeTree('astra',shotastra)
    ROG1=ROG1/1e3#go to kA
    plt.figure('Rogowski kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    for j in range(0,ni):
        if ni==1:plt.plot(T,ROG1,label=ROGnam[index[j]-1]+'#'+str(shotastra)+'@'+run)
        if ni>1:plt.plot(T,ROG1[j],label=ROGnam[index[j]-1]+'#'+str(shotastra)+'@'+run)
def plot_rog_astra_all(index,shotastra,run):
    index_rog=[8,9,15,16,21,25,12,13,1,2,6,10,17,27,7,3,11,30,4,5,28,29,17,31]
    ni=len(index)
    if ni == 0: return
    conn.openTree('astra',shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:I'
    try:
        ROG=conn.get(signame)
        conn.closeTree('astra',shotastra)
    except:
        return
    ROG=ROG/1e3#go to kA
    plt.figure('Rogowski kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    for j in range(0,ni):
        print(ROGnam[index[j]-1],index[j],index_rog[index[j]-1])
        plt.plot(T,ROG[:,index_rog[index[j]-1]-1],label=ROGnam[index[j]-1]+'#'+str(shotastra)+'@'+run)
def plot_rogname_astra_all(name,shotastra,run):
    conn.openTree('astra',shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:NAME'
    ROGNAME=conn.get(signame)
    ROGNAMEs=[j.strip() for j in ROGNAME]
    index=ROGNAMEs.index(name)
    signame=run+'.ROG.ALL:I'
    ROG=conn.get(signame)
    conn.closeTree('astra',shotastra)
    ROG=ROG/1e6#go to kA
    print(ROGNAMEs[index],index)        
    plt.plot(T,ROG[:,index],label=ROGNAMEs[index]+'#'+str(shotastra)+'@'+run)

def plot_ipl_rog_astra_all(shotastra,run):
#           1         2         3         4        5     6      7         8
#ROGnam=['DIVPSRB','DIVPSRT','HFSPSRB','HFSPSRT','MCB','MCT','GASBFLB','GASBFLT']
    index=[1,2,3,4,5,6,7,8]
    index_rog=[8,9,15,16,21,25,12,13,1,2,6,10,17,27,7,3,11,30,4,5,28,29,17,31]
    conn.openTree('astra',shotastra)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:I'
    ROG=conn.get(signame)
    NAME=conn.get(run+'.ROG.ALL:NAME')
    SUM=0*ROG[:,0]
    for j in index:
        print(NAME[index_rog[j-1]-1])
        SUM=SUM+ROG[:,index_rog[j-1]-1]
    j=13
    print(NAME[index_rog[j-1]-1])
    IPL=(ROG[:,index_rog[j-1]-1]-SUM)/1000
    conn.closeTree('astra',shotastra)
    plt.figure('Rogowski kA',figsize=(10, 3))
    plt.rc('font', size=FONTSIZE)
    plt.plot(T,IPL,label='IPL from Rogowski, kA #'+str(shotastra)+'@'+run)

def plot_ipl_astra(shotastra,run):
    conn.openTree('astra',shotastra)
    T=conn.get(run+':TIME')
    signame=run+'.GLOBAL:IPL'
    IPL= conn.get(signame).data()/1000
    conn.closeTree('astra',shotastra)
    plt.plot(T,IPL,label='GLOBAL:IPL , kA #'+str(shotastra)+'@'+run)
def read_rogefit_astra_all(shotastra,run):
    index_efit=[20,24,1,0,16,9,5,8,7,15,14,12,11]
    conn.openTree('astra',shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:'
    try:
        VAR=conn.get(signame+'I')
        NAME=conn.get(signame+'NAME')
        conn.closeTree('astra',shotastra)
    except:
        return 0,0
    ROG=VAR[:,index_efit]
    return T,ROG
def read_rogefit_tree(treename,shotastra,run):
    index_efit=[20,24,1,0,16,9,5,8,7,15,14,12,11]
    conn.openTree(treename,shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:'
    try:
        VAR=conn.get(signame+'I')
        NAME=conn.get(signame+'NAME')
        conn.closeTree(treename,shotastra)
    except:
        return 0,0
    ROG=VAR[:,index_efit]
    return T,ROG
def read_rog_tree(treename,name,shotastra,run):
    conn.openTree(treename,shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    T=conn.get(run+':TIME')
    signame=run+'.ROG.ALL:'
    try:
        VAR=conn.get(signame+'I')/1e3
        NAME=conn.get(signame+'NAME')
        conn.closeTree(treename,shotastra)
        index=-1
        for i in range(0,len(NAME)):
            if NAME[i] == 'ROG_'+name: index=i
        if index==-1: print('No such Rogowski name: '+name+' in tree: '+treename)
        if index==-1: return 0,0,''
    except:
        return 0,0,''
    #index2=index.astype(int)
    return T,VAR[:,index]
def read_rog_tree_all(treename,shotastra,run):
    conn.openTree(treename,shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    try:
        T=conn.get(run+':TIME')
        signame=run+'.ROG.ALL:'
        VAR=conn.get(signame+'I')/1e3
        NAME=conn.get(signame+'NAME')
        conn.closeTree(treename,shotastra)
    except:
        return 0,0,''
    return T,VAR,NAME
def read_rogname_astra_all(name,shotastra,run,t1,t2):
    conn.openTree('astra',shotastra)
    print('ASTRA shot #'+str(shotastra)+'@'+run)
    TIME=conn.get(run+':TIME')
    iupa=np.where(TIME > t2)
    iup=iupa[0][0]
    idwa=np.where(TIME < t1)
    idw=idwa[0][len(idwa[0])-1]
    signame=run+'.ROG.ALL:NAME'
    ROGNAME=conn.get(signame)
    ROGNAMEs=[j.strip() for j in ROGNAME]
    index=ROGNAMEs.index('ROG_'+name)
    signame=run+'.ROG.ALL:I'
    ROG=conn.get(signame)
    conn.closeTree('astra',shotastra)
    ROG=ROG/1e3
    print(ROGNAMEs[index],index)        
    return TIME[idw:iup],ROG[idw:iup,index]
def read_rog_exp(ROGNAME,shot,t1,t2):
    BEST='BEST.'
    print('ST40:'+str(shot))
    conn.openTree('ST40',shot)
    TIME=conn.get('dim_of(MAG.'+BEST+'ROG.TFWIRE:I)').data()
    iupa=np.where(TIME > t2)
    iup=iupa[0][0]
    idwa=np.where(TIME < t1)
    idw=idwa[0][len(idwa[0])-1]
    signame='MAG.'+BEST+'ROG.'+ROGNAME+':I'
    ROG=conn.get(signame).data()
    ROG=ROG/1e3#go to kA
    conn.closeTree('st40',shot)

    return TIME[idw:iup],ROG[idw:iup]
