import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
conn = Connection('192.168.1.7:8000')
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
count=0
shotefit=11560
runefit='BEST'
timeefit=0.1
shotelmag=206
filename='settings/default/'
index=[1,3,5,7,8]
def read_EFIT_RZ(shotelmag):
    R0,Z0,dr0,dz0,BASIS0=read_basis(shotelmag)
    NAME4,R4,Z4,dr4,dz4,BASIS4=read_basis_add()
    VAR=np.zeros((BASIS0.shape[0]+4,BASIS0.shape[1]+len(BASIS4))) 
    VAR4=np.zeros((4,len(BASIS4)))
    ii=0
    factor=[1.22,1.22,1,1]
    VAR4[0,0]=BASIS4[0]/factor[ii]
    for j in range(1,len(BASIS4)):                              
        if NAME4[j] != NAME4[j-1]:ii+=1
        VAR4[ii,j]=BASIS4[j]/factor[ii]
    VAR[:BASIS0.shape[0],:BASIS0.shape[1]]=BASIS0
    VAR[BASIS0.shape[0]:,BASIS0.shape[1]:]=VAR4
        
    Re=np.append(R0,R4)
    Ze=np.append(Z0,Z4)
    dre=np.append(dr0,dr4)
    dze=np.append(dz0,dz4) 
    print('EFIT RZ read')
    return Re,Ze,dre,dze,VAR
def read_basis(shotelmag):
    shotpfit=202
    conn.openTree('PFIT',shotpfit)
    signal='PRESHOT.FOR_POST:VESSEL_BASIS'
    VAR=conn.get(signal)#(24,786)
    conn.closeTree('PFIT',shotpfit)
    conn.openTree('ELMAG',shotelmag)
    signal='VESSEL:'
    R=conn.get(signal+'R') #786
    Z=conn.get(signal+'Z')
    dr=conn.get(signal+'DR')
    dz=conn.get(signal+'DZ')
    conn.closeTree('ELMAG',shotelmag)
    return R,Z,dr,dz,VAR
def read_efit_coils():
    conn.openTree('ELMAG',shotelmag)
    signal='COILS:'
    R=conn.get(signal+'R') 
    Z=conn.get(signal+'Z')
    DR=conn.get(signal+'DR') 
    DZ=conn.get(signal+'DZ')
    c=conn.get(signal+'CIRCUITS')
    names=conn.get(signal+'NAMES')
    conn.closeTree('ELMAG',shotelmag)
    for i in range(len(names)):
        nn=sum(c[:,i])
        meanr=sum(R*c[:,i])/nn
        meanz=sum(Z*c[:,i])/nn
        dr=2*(max(R*c[:,i])-meanr)+sum(DR*c[:,i])/nn
        dz=2*(max(Z*c[:,i])-meanz)+sum(DZ*c[:,i])/nn
        print(i,names[i],meanr,meanz,dr,dz)

def read_basis_add():
    filename='/home/alexei.dnestrovskij/astra_project/astra_work/pyt/settings/ST40_P2p3C1_Magnetic/ST40_201_data/PFCpassive_add'
    R=np.array([])
    Z=np.array([])
    dr=np.array([])
    dz=np.array([])
    NAME=np.array([])
    index=np.array([])
    f = open(filename, "r")
    f.readline()
    while True:
        aa=f.readline()
        aa=f.readline()
        if not aa : break
        name=aa.split()[0]
        aa=f.readline()
        nl=int(aa.split()[0])
        aa=f.readline()
        for i in range(0,nl):
            aa=f.readline()
            NAME=np.append(NAME,name)
            index=np.append(index,int(aa.split()[1]))
            R=np.append(R,float(aa.split()[2]))
            Z=np.append(Z,float(aa.split()[3]))
            dr=np.append(dr,float(aa.split()[4]))
            dz=np.append(dz,float(aa.split()[5]))
    nfil=R.shape[0]
    nvar=np.array([])
    ii=0
    for i in range(1,nfil):
        if NAME[i] != NAME[i-1]:
            ii+=1
            nvar=np.append(nvar,i)
    nvar=np.append(nvar,i+1)
    VAR=np.array([]) 
    ii=0
    nn=nvar[0]
    for i in  range(0,nfil):
        if i >= nvar[ii]:
            ii+=1
            nn=nvar[ii]-nvar[ii-1]
            #print(ii,nn)
        VAR=np.append(VAR,dr[i]*dz[i]/nn)
        #print(NAME[i],VAR[i],dr[i]*dz[i],nn)
    return NAME,R,Z,dr,dz,VAR
def plot_passives(ax,R,Z,dr,dz,VAR,ivc,index,shotefit,runefit,timeefit,count):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:]
    NAMEVES=NAME1[12:27]
    ROG=VAR1[:,27:40]
    ROGBAS=VAR[15:,:]
    NAMESTR=NAME1[27:]
    PASS=VES[t1,:]@VESBAS
    print('Current in VESSEL, kA',sum(PASS)*1000)
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    if ivc :
        #PASS=0*VESBAS[0,:]
        for i in range(0,len(NAMEVES)):
            #PASS=PASS+VES[t1,i]*VESBAS[i,:]
            EIGCUR=sum(VES[t1,i]*VESBAS[i,:])
            if abs(EIGCUR) > 0.00001 : #10kA
                print(NAMEVES[i].strip(),'DOF:',VES[t1,i],'Current in EIGs, kA:',EIGCUR*1000)
        print('Current in VESSEL, kA:',sum(PASS)*1000)
        ax.scatter3D(R,Z,PASS/dr/dz,zdir='z',c=col[count],marker='.',label='EFIT:'+str(shotefit)+'@'+runefit+'time='+str(TIME[t1]))
        for i in range(len(R)):
            if PASS[i] != 0:
                ax.plot([R[i],R[i]],[Z[i],Z[i]],[PASS[i]/dr[i]/dz[i],0],col[count])
    print(index)
    for i in index:        
        print(NAMESTR[i].strip())
        if   NAMESTR[i].strip()[len(NAMESTR[i].strip())-1] == 'T':
            j=0
        elif NAMESTR[i].strip()[len(NAMESTR[i].strip())-1] == 'B':
            j=-1
        else:
            j=1
        if j==0 or j==-1:
            nfil=0
            for j2 in [i+j,i+j+1]:
                #print(np.array(ROGBAS[j2,:]/dr/dz)[np.array((np.where(ROGBAS[j2,:]/dr/dz!=0)))])
                #print(NAMESTR[j2].strip(),np.array((np.where(ROGBAS[j2,:]/dr/dz!=0))).shape[1])
                #print(NAMESTR[j2].strip()+' sum(BASIS/dr/dz): ',end='')
                #print(np.sum(np.array(ROGBAS[j2,:]/dr/dz)[np.array((np.where(ROGBAS[j2,:]/dr/dz!=0)))]))
                nfil=nfil+np.array(ROGBAS[j2,:]/dr/dz)[np.array((np.where(ROGBAS[j2,:]/dr/dz!=0)))].shape[1]
                print(NAMESTR[j2].strip(),'Number of filaments',nfil)
        
        TOTCUR=sum(ROG[t1,i]*ROGBAS[i,:])*1000
        if abs(TOTCUR) >=0:#0.001: #1A
            count+=1
            area=0
            for ii in range(len(R)):
                if ROGBAS[i,ii] != 0:
                    area+=dr[ii]*dz[ii]
                    ax.plot([R[ii],R[ii]],[Z[ii],Z[ii]],[ROG[t1,i]*ROGBAS[i,ii]/dr[ii]/dz[ii],0],col[count])
                    #print(i,ii,NAMESTR[i].strip()[6:],dr[ii]*dz[ii]/ROGBAS[i,ii]/nfil,ROGBAS[i,ii],dr[ii]*dz[ii]/nfil*2)
                    #print(i,ii,NAMESTR[i].strip()[6:],dr[ii],dz[ii])
            print(NAMESTR[i].strip()[6:],'DOF:',ROG[t1,i],'Total current in filament structure, kA:',TOTCUR,'Area:',area*1e4,'cm^2')

def read_passives(VAR,ivc,index,shotefit,runefit,timeefit):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:]
    NAMEVES=NAME1[12:27]
    ROG=VAR1[:,27:40]
    ROGBAS=VAR[15:,:]
    NAMESTR=NAME1[27:]
    if ivc : 
        PASS=VES[t1,:]@VESBAS
    else:
        PASS=0*VESBAS[0,:]
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    print('IVC included:',ivc,'Current in VESSEL, kA',sum(PASS)*1000)
    ind=np.array(index).astype(int) 
    for i in ind:
        TOTCUR=sum(ROG[t1,i]*ROGBAS[i,:])*1000
        for ii in range(len(ROGBAS[0,:])): 
            if ROGBAS[i,ii] != 0: 
                PASS[ii]=ROG[t1,i]*ROGBAS[i,ii]
                print(i,ii,NAMESTR[i].strip()[6:],PASS[ii],ROGBAS[i,ii])
        print('Total current in filament structure, kA:',NAMESTR[i].strip()[6:],TOTCUR)
        print('Sum of BASIS:',sum(ROGBAS[i,:]))
    return PASS
def read_active(shotefit,runefit,timeefit):
    indexspider=[3,8,1,4,6,7,0] #MC  PSH DIV BVL BVUT BVUB SOL 
    ind2=np.array(indexspider).astype(int) 
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    name1=np.array([])
    CURR=np.array([])
    CURR=np.append(CURR,0.0)
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    print('IPL ',CURR[0])
    for i in ind2:
                      print(NAME[i].strip(),VAR[t1,i])
                      name1=np.append(name1,NAME[i].strip())
                      CURR=np.append(CURR,VAR[t1,i])
    return CURR

def plot_basis(ax,R,Z,dr,dz,VAR,ivc,index,shotefit,runefit,timeefit,count):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    nves=np.array(np.where(VAR[0,:]!=0)).shape[1]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:nves]
    NAMEVES=NAME1[12:27]
    PASS=VES[t1,:]@VESBAS
    print('Current in VESSEL, kA',sum(PASS)*1000)
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    if ivc :
        for j in index:
            i=j-1
            EIGCUR=sum(VES[t1,i]*VESBAS[i,:])
            print(NAMEVES[i].strip(),'DOF:',VES[t1,i],'SumEig:',sum(VESBAS[i,:]),'Current in EIGs, kA:',EIGCUR*1000)
            ax.scatter3D(R[:nves],Z[:nves],VESBAS[i,:],zdir='z',c=col[count],marker='.',label=NAMEVES[i].strip()+'Basis')
            for ii in range(nves):
                if VESBAS[i,ii] != 0:
                    ax.plot([R[ii],R[ii]],[Z[ii],Z[ii]],[VESBAS[i,ii],0],col[count])
            count+=1

def plot_ivc(ax,R,Z,dr,dz,VAR,ivc,index,shotefit,runefit,timeefit,count):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    nves=np.array(np.where(VAR[0,:]!=0)).shape[1]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:nves]
    NAMEVES=NAME1[12:27]
    PASS=VES[t1,:]@VESBAS
    print('Current in VESSEL, kA',sum(PASS)*1000)
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    if ivc :
        for j in index:
            i=j-1
            EIGCUR=sum(VES[t1,i]*VESBAS[i,:])
            print(NAMEVES[i].strip(),'DOF:',VES[t1,i],'SumEig:',sum(VESBAS[i,:]),'Current in EIGs, kA:',EIGCUR*1000)
            ax.scatter3D(R[:nves],Z[:nves],VES[t1,i]*VESBAS[i,:],zdir='z',c=col[count],marker='.',label=NAMEVES[i].strip()+'Basis*DOF')
            for ii in range(nves):
                if VESBAS[i,ii] != 0:
                    ax.plot([R[ii],R[ii]],[Z[ii],Z[ii]],[VES[t1,i]*VESBAS[i,ii],0],col[count])
            count+=1
def plot_ivc_dens(ax,R,Z,dr,dz,VAR,ivc,index,shotefit,runefit,timeefit,count):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    nves=np.array(np.where(VAR[0,:]!=0)).shape[1]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:nves]
    NAMEVES=NAME1[12:27]
    PASS=VES[t1,:]@VESBAS
    print('Current in VESSEL, kA',sum(PASS)*1000)
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    if ivc :
        for j in index:
            i=j-1
            EIGCUR=sum(VES[t1,i]*VESBAS[i,:])
            print(NAMEVES[i].strip(),'DOF:',VES[t1,i],'SumEig:',sum(VESBAS[i,:]),'Current in EIGs, kA:',EIGCUR*1000)
            ax.scatter3D(R[:nves],Z[:nves],VES[t1,i]*VESBAS[i,:]/dr[:nves]/dz[:nves],zdir='z',c=col[count],marker='.',label=NAMEVES[i].strip()+'Basis*DOF/dr/dz')
            for ii in range(nves):
                if VESBAS[i,ii] != 0:
                    ax.plot([R[ii],R[ii]],[Z[ii],Z[ii]],[VES[t1,i]*VESBAS[i,ii]/dr[ii]/dz[ii],0],col[count])
            count+=1


"""
np.array(ROGBAS[0,:]/dr/dz)[np.array((np.where(ROGBAS[0,:]/dr/dz!=0)))] 
for i in [0,2,4,6,9,11]:
    print(np.array(ROGBAS[i,:]/dr/dz)[np.array((np.where(ROGBAS[i,:]/dr/dz!=0)))])
    print(NAME[i],np.array((np.where(ROGBAS[i,:]/dr/dz!=0))).shape[1])
    print(np.array(ROGBAS[i+1,:]/dr/dz)[np.array((np.where(ROGBAS[i+1,:]/dr/dz!=0)))])
    print(NAME[i+1],np.array((np.where(ROGBAS[i+1,:]/dr/dz!=0))).shape[1])
    print(NAME[i]+' and '+NAME[i+1]+' sum(BASIS/dr/dz): ',end='')
    print(np.sum(np.array(ROGBAS[i,:]/dr/dz)[np.array((np.where(ROGBAS[i,:]/dr/dz!=0)))])+np.sum(np.array(ROGBAS[i+1,:]/dr/dz)[np.array((np.where(ROGBAS[i+1,:]/dr/dz!=0)))]))
"""
def read_IVC_names(num):
    #num=7 # for supports
    NAME0=["'_IVC_1'","'IVC_12_thick'","'IVC_2'","'IVC_23_thick'","'IVC_3'","'IVC_34_thick'","'IVC_4'","'IVC_4_support'","'IVC_45_thick'","'IVC_5'"]
    filename='/home/alexei.dnestrovskij/astra_project/astra_work/pyt/settings/ST40_P2p3C1_Magnetic/ST40_201_data/PFCpassive_reordered'
    ind=np.array([])
    R=np.array([])
    Z=np.array([])
    dr=np.array([])
    dz=np.array([])
    NAME=np.array([])
    index=np.array([])
    f = open(filename, "r")
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    while True:
        aa=f.readline()
        if aa[0] == '+':break 
        aa=f.readline()
        #if not aa : break
        nl=int(aa.split()[0])
        name=aa.split()[1]
        for i in range(0,nl):
            aa=f.readline()
            NAME=np.append(NAME,name)
            index=np.append(index,int(aa.split()[0]))
            R=np.append(R,float(aa.split()[1]))
            Z=np.append(Z,float(aa.split()[2]))
            dr=np.append(dr,float(aa.split()[3]))
            dz=np.append(dz,float(aa.split()[4]))
    NAMELINE=''
    for i in num:
        ind0=index[np.where(NAME==NAME0[i])]
        ind=np.append(ind,ind0)
        NAMELINE=NAMELINE+' '+NAME0[i]
        #plt.plot(R,Z,'r+')
        #plt.plot(R[np.where(NAME=="'IVC_4_support'")],Z[np.where(NAME=="'IVC_4_support'")],'b+')
        #plt.show()
    ind2=ind.astype(int)
    return ind2,NAMELINE
def read_ivc_current(R,Z,dr,dz,VAR,indr,shotefit,runefit,timeefit):
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR1=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME1=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    nves=np.array(np.where(VAR[0,:]!=0)).shape[1]
    VES=VAR1[:,12:27]
    VESBAS=VAR[:15,:nves]
    NAMEVES=NAME1[12:27]
    PASS=VES[t1,:]@VESBAS*1000
    print('Current in VESSEL, kA',sum(PASS))
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    ind0,NAME=read_IVC_names(indr)
    print('Name of structures',NAME)
    print('Current in IVC structure Bottom, kA',sum(PASS[ind0]))
    print('Current in IVC structure    Top, kA',sum(PASS[ind0-1]))
def read_efit_coils_filaments(shotelmag):
    conn.openTree('ELMAG',shotelmag)
    signal='COILS:'
    R=conn.get(signal+'R') 
    Z=conn.get(signal+'Z')
    DR=conn.get(signal+'DR') 
    DZ=conn.get(signal+'DZ')
    c=conn.get(signal+'CIRCUITS')
    names=conn.get(signal+'NAMES')
    conn.closeTree('ELMAG',shotelmag)
    ii=0
    nn=sum(c[:,0])
    for i in range(len(R)):
        if i > nn-1 : 
            ii+=1
            nn=nn+sum(c[:,ii])
        #print(i,nn,R[i],Z[i],DR[i],DZ[i],names[ii])
        print('1 ',R[i],Z[i],DR[i],DZ[i],' 690D-9 0 ',names[ii])
def read_active364(shotefit,runefit,timeefit):
    conn.openTree('ELMAG',shotelmag)
    signal='COILS:'
    c=conn.get(signal+'CIRCUITS')
    names=conn.get(signal+'NAMES')
    conn.closeTree('ELMAG',shotelmag)
    conn.openTree('EFIT',shotefit)
    signame0=runefit
    signame=runefit+'.CONSTRAINTS.PFC_DOF:'
    try:
        TIME=conn.get(signame0+':TIME')#nt
        VAR=conn.get(signame+'CVALUE')/1e6#nt,40
        NAME=conn.get(signame+'NAME')#nt,40
    except:
        print('Could not read EFIT run',shotefit,runefit)
        #return
    t=np.where(TIME>timeefit) 
    t1=t[0][0]
    name1=np.array([])
    CURR=np.array([])
    ii=0
    nn=sum(c[:,0])
    print('EFIT:',shotefit,'@',runefit,'time=',TIME[t1])
    for i in range(len(c[:,0])):
        if i > nn-1 : 
            ii+=1
            nn=nn+sum(c[:,ii])
#        print(i,nn,NAME[ii].strip(),VAR[t1,ii])
        name1=np.append(name1,NAME[ii].strip())
        CURR=np.append(CURR,VAR[t1,ii])
    return CURR





    filename='/home/alexei.dnestrovskij/astra_project/astra_work/pyt/settings/ST40_P2p3C1_Magnetic/ST40_201_data/PFCpassive_reordered'
    f = open(filename, "r")
    fw=open("fires.dat", "w")
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    k=0
    while True:
        aa=f.readline()
        if aa[0] == '+':break 
        aa=f.readline()
        #if not aa : break
        nl=int(aa.split()[0])
        name=aa.split()[1]
        name1=name[1:len(name)-1]
        if name1[0] == '_':name1=name1[1:]
        R=np.array([])
        Z=np.array([])
        dr=np.array([])
        dz=np.array([])
        for i in range(0,nl):
            aa=f.readline()            
            index=int(aa.split()[0])
            R=np.append(R,float(aa.split()[1]))
            Z=np.append(Z,float(aa.split()[2]))
            dr=np.append(dr,float(aa.split()[3]))
            dz=np.append(dz,float(aa.split()[4]))
        if name1[len(name1)-5:] == 'thick':
            k+=1
            R1=np.mean(R);Z1=np.mean(Z);dr1=np.sqrt(sum(dr*dz));dz1=dr1
            print('1 '+str(R1)+' '+str(Z1)+' '+str(dr1)+' '+str(dz1)+' 690D-9 0 '+name1+'T')
            fw.write('1 '+str(R1)+' '+str(Z1)+' '+str(dr1)+' '+str(dz1)+' 690D-9 0 '+name1+'T'+'\n')
            k+=1
            print('1 '+str(R1)+' -'+str(Z1)+' '+str(dr1)+' '+str(dz1)+' 690D-9 0 '+name1+'B')
            fw.write('1 '+str(R1)+' -'+str(Z1)+' '+str(dr1)+' '+str(dz1)+' 690D-9 0 '+name1+'B'+'\n')
        else:
            R1=np.array([])
            Z1=np.array([])
            dr1=np.array([])
            dz1=np.array([])
            if int(nl/2)*2 == nl:
                for i in range(0,nl,2):
                    R1=np.append(R1,0.5*(R[i]+R[i+1]))
                    Z1=np.append(Z1,0.5*(Z[i]+Z[i+1]))
                    dr1=np.append(dr1,np.sqrt(dr[i]*dz[i]+dr[i+1]*dz[i+1]))
                    dz1=np.append(dz1,np.sqrt(dr[i]*dz[i]+dr[i+1]*dz[i+1]))
            else:
                for i in range(0,nl-1,2):
                    R1=np.append(R1,0.5*(R[i]+R[i+1]))
                    Z1=np.append(Z1,0.5*(Z[i]+Z[i+1]))
                    dr1=np.append(dr1,np.sqrt(dr[i]*dz[i]+dr[i+1]*dz[i+1]))
                    dz1=np.append(dz1,np.sqrt(dr[i]*dz[i]+dr[i+1]*dz[i+1]))
                R1=np.append(R1,R[i+1])
                Z1=np.append(Z1,Z[i+1])
                dr1=np.append(dr1,np.sqrt(dr[i+1]*dz[i+1]))
                dz1=np.append(dz1,np.sqrt(dr[i+1]*dz[i+1]))                
            for i in range(0,len(R1)): 
                k+=1
                print('1 '+str(R1[i])+' '+str(Z1[i])+' '+str(dr1[i])+' '+str(dz1[i])+' 690D-9 0 '+name1+'T')
                fw.write('1 '+str(R1[i])+' '+str(Z1[i])+' '+str(dr1[i])+' '+str(dz1[i])+' 690D-9 0 '+name1+'T'+'\n')
            for i in range(0,len(R1)): 
                k+=1
                print('1 '+str(R1[i])+' -'+str(Z1[i])+' '+str(dr1[i])+' '+str(dz1[i])+' 690D-9 0 '+name1+'B')
                fw.write('1 '+str(R1[i])+' -'+str(Z1[i])+' '+str(dr1[i])+' '+str(dz1[i])+' 690D-9 0 '+name1+'B'+'\n')
            #fw.write('1 '+str(R[i])+' '+str(Z[i])+' '+str(dr[i])+' '+str(dz[i])+' 690D-9 0 '+name1+'T'+'\n')
        #for i in range(0,nl):
            #k+=1
            #print('1 '+str(R[i])+' -'+str(Z[i])+' '+str(dr[i])+' '+str(dz[i])+' 690D-9 0 '+name1+'B')
            #fw.write('1 '+str(R[i])+' -'+str(Z[i])+' '+str(dr[i])+' '+str(dz[i])+' 690D-9 0 '+name1+'B'+'\n')
#    fw.close()

#fw.write('1 '+str(Re[i])+' '+str(Ze[i])+' '+str(dre[i])+' '+str(dze[i])+' 690D-9 0 '+name+'\n')
