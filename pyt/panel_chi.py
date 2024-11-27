# python3 pyt/panel_chi.py&
import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import bpprobe_functions as b
import floop_functions as f
import rog_functions as rog
import read_efit_data as efit
import passives_EFIT as passives
import read_efit_data as efit
from scipy import interpolate
#this data from #12515 EFIT.CONSTRAINTS
shotefit=12515
runE='BEST'
loopefit=["PSI_FLOOP_001 ","PSI_FLOOP_002 ","PSI_FLOOP_003 ","PSI_FLOOP_004 ","PSI_FLOOP_005 ","PSI_FLOOP_006 ","PSI_FLOOP_007 ","PSI_FLOOP_008 ","PSI_FLOOP_009 ","PSI_FLOOP_010 ","PSI_FLOOP_011 ","PSI_FLOOP_012 ","PSI_FLOOP_013 ","PSI_FLOOP_014 ","PSI_FLOOP_015 ","PSI_FLOOP_016 ","PSI_FLOOP_017 ","PSI_FLOOP_018 ","PSI_FLOOP_019 ","PSI_FLOOP_020 ","PSI_FLOOP_021 ","PSI_FLOOP_022 ","PSI_FLOOP_023 ","PSI_FLOOP_024 ","PSI_FLOOP_025 ","PSI_FLOOP_026 ","PSI_FLOOP_027 ","PSI_FLOOP_029 ","PSI_FLOOP_030 ","PSI_FLOOP_101 ","PSI_FLOOP_102 ","PSI_FLOOP_103 ","PSI_FLOOP_104 ","PSI_FLOOP_105 ","PSI_FLOOP_106 ","PSI_FLOOP_201 ","PSI_FLOOP_202 ","PSI_FLOOP_203 ","PSI_FLOOP_210 ","PSI_FLOOP_211 ","PSI_FLOOP_212 "]

probefit=["B_BPPROBE_101 ","B_BPPROBE_102 ","B_BPPROBE_103 ","B_BPPROBE_104 ","B_BPPROBE_105 ","B_BPPROBE_106 ","B_BPPROBE_107 ","B_BPPROBE_108 ","B_BPPROBE_109 ","B_BPPROBE_110 ","B_BPPROBE_111 ","B_BPPROBE_112 ","B_BPPROBE_113 ","B_BPPROBE_114 ","B_BPPROBE_115 ","B_BPPROBE_116 ","B_BPPROBE_117 ","B_BPPROBE_118 ","B_BPPROBE_119 ","B_BPPROBE_120 ","B_BPPROBE_121 ","B_BPPROBE_122 ","B_BPPROBE_123 ","B_BPPROBE_124 ","B_BPPROBE_125 ","B_BPPROBE_126 ","B_BPPROBE_127 ","B_BPPROBE_128 ","B_BPPROBE_129 ","B_BPPROBE_130 ","B_BPPROBE_131 ","B_BPPROBE_132 ","B_BPPROBE_133 ","B_BPPROBE_134 "]

rogefit=["I_ROG_MCT ","I_ROG_MCB ","I_ROG_BVLT ","I_ROG_BVLB ","I_ROG_INIVC000 ","I_ROG_DIVT ","I_ROG_DIVB ","I_ROG_DIVPSRT ","I_ROG_DIVPSRB ","I_ROG_HFSPSRT ","I_ROG_HFSPSRB ","I_ROG_GASBFLT ","I_ROG_GASBFLB "]


name1=0
index=0
flatopvac=[11689,11698,11690,11699,11691,11702,11692,11700,11693,11701]
n1=30;n2=6;n3=3;n4=3
nloop=n1+n2+n3+n4
nameloop=np.array([])
nameloop0=np.array([])
for i in range(0,n1):
          if i<9:
                    nameloop=np.append(nameloop,'FLOOP_00'+str(i+1))
                    nameloop0=np.append(nameloop0,'00'+str(i+1))
          elif i != 27:
                    nameloop=np.append(nameloop,'FLOOP_0'+str(i+1))
                    nameloop0=np.append(nameloop0,'0'+str(i+1))
for i in range(100,100+n2):nameloop=np.append(nameloop,'FLOOP_'+str(i+1))
for i in range(100,100+n2):nameloop0=np.append(nameloop0,str(i+1))
for i in range(200,200+n3):nameloop=np.append(nameloop,'FLOOP_'+str(i+1))
for i in range(200,200+n3):nameloop0=np.append(nameloop0,str(i+1))
for i in range(209,209+n4):nameloop=np.append(nameloop,'FLOOP_'+str(i+1))
for i in range(209,209+n4):nameloop0=np.append(nameloop0,str(i+1))
nameloops=nameloop0.tolist()
nprob=34;nameprobe=np.array([]);nameprobe0=np.array([])
for i in range(0,nprob):
          nameprobe=np.append(nameprobe,'BPPROBE_'+str(101+i))
          nameprobe0=np.append(nameprobe0,str(101+i))
nameprobes=nameprobe0.tolist()
namerog=['MCT','MCB','BVLT','BVLB','INIVC000','DIVT','DIVB','GASBFLT','GASBFLB','HFSPSRT','HFSPSRB','DIVPSRT','DIVPSRB']#,'MCWIRE','DIVBWIRE','BVLWIRE','DIVTWIRE','SOLWIRE','BVUBWIRE','BVUTWIRE','PSHBWIRE','PSHTWIRE']
nrog=len(namerog)
namerog=np.array(namerog)
namerog0=namerog
namerogs=namerog0.tolist()
combo_style1={'size':(5,1)}
combo_style3={'size':(12,1)}
combobox1=sg.InputCombo(values=nameprobes, **combo_style1, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=nameloops, **combo_style1, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=namerogs, **combo_style3, enable_events=True, key='-COMBO3-')

conn = Connection('192.168.1.7:8000')
shotastra=13011689
RUN='RUN02'
shotst40=11689
shotelmag=206
FONTSIZE=12
treename='ASTRA'
time=-0.3
time1=-0.31
time2=-0.3
r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',shotastra).getNode("\\TOP.RUN02.GLOBAL").getNodeWild('*').getPath().data()
run=np.array([])
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    print(el) 
    run = np.append(run,el)

runs=run.tolist()

combo_style={'size':(12,1)}

comboboxr=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO0-')
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))],
          [sg.T("ST40 shot ="), sg.Input('11689', size=(6,1),key="-SHOT-")],
          [sg.Radio('ASTRA', "RADIO3",default=True, key="-astra-"),
           sg.Radio('SPIDER', "RADIO3",default=False, key="-spider-"),
           sg.T("ASTRA shot="), sg.Input('13011689', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),comboboxr,
           sg.Button('HELPrun',size=(10,1))],
          [sg.T('shotlist:'),sg.Radio('flattop', "RADIO0", default=True, key="-flattop-")],
          [sg.T("time1="), sg.Input('-0.31', size=(7,1), key="-time1-"),
           sg.T("time2="), sg.Input('-0.3', size=(7,1), key="-time2-")],
          [sg.Radio('BPPROBES', "RADIO1",default=True, key="-bprobes-"),
           sg.Radio('FL_LOOPS', "RADIO1",default=False, key="-floops-"),
           sg.Radio('ROG', "RADIO1",default=False, key="-rog-")],
          [sg.Radio('plot over sensor', "RADIO2",default=True, key="-plot1-"),
           sg.Radio('plot over time', "RADIO2",default=False, key="-plot2-"),
           sg.Radio('plot R,Z', "RADIO2",default=False, key="-plot3-"),
           sg.Radio('shotlist', "RADIO2",default=False, key="-list-")],
          [sg.T("BPROBE:"),combobox1,sg.T("FLOOP:"),combobox2,sg.T("ROG:"),combobox3],
          [sg.Checkbox('overplot',default=False, key="-overplot-")],
          [sg.T("")]]

window = sg.Window('magnetics exp vs calc', layout, size=(715, 500))
while True:
    plt.rc('font', size=FONTSIZE)
    event, values = window.read()
    shotastra=int(values["-shot-"])
    shotst40=int(values["-SHOT-"])
    time1=float(values["-time1-"])
    time2=float(values["-time2-"])
    time=0.5*(time1+time2)
    if values["-astra-"]== True : treename='ASTRA'
    if values["-spider-"]== True : treename='SPIDER'
    if values['-flattop-']==True:shots=flatopvac
    n1=13
    if treename == "ASTRA": n1=12
    if  values["-bprobes-"] == True:  
        magname='BP'
        num=8
        name=nameprobe
        bottom=0.2
        rotation=70
        facw=50
    if  values["-floops-"] == True: 
        magname='FLUX'
        num=6
        name=nameloop
        bottom=0.2
        rotation=70
        facw=10
    if  values["-rog-"] == True: 
        num=0
        magname='ROGC'
        name=namerog
        bottom=0.3
        rotation=30
        facw=5
    nc=len(name)
    name0=np.array([])
    for i in range(nc):
        name0=np.append(name0,name[i].strip()[num:])
    if event == "reread shot":
        r=Tree(treename,shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][n1:20].decode().strip()
            print(el)
            run = np.append(run,el)
        runs=run.tolist()
        comboboxr.Update(values=runs)
    if event == '-COMBO0-' :
        RUN= values['-COMBO0-']
#        print(RUN+':HELP')
        conn.openTree(treename,shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
    if event == '-COMBO1-' and values["-bprobes-"] == True : 
        name1=values['-COMBO1-']
        index=np.where(name1==nameprobe0)[0][0]
    if event == '-COMBO2-' and values["-floops-"] == True : 
        name1=values['-COMBO2-']
        index=np.where(name1==nameloop0)[0][0]
    if event == '-COMBO3-' and values["-rog-"] == True : 
        name1=values['-COMBO3-']
        index=np.where(name1==namerog0)[0][0]
    print(name1)
        
    if event == "HELPrun":
        r=Tree(treename,shotastra).getNode("\\TOP").getChildren().getPath().data()
        for i in range(0,len(r)):
            run=r[i][n1:20].decode().strip()
            print(run+':HELP')
            if(run != 'HELP'):
                text=conn.get(run+':HELP')
                print(run+': ',text)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        if values["-overplot-"] == False : 
            if values["-list-"] == True :fig=plt.figure(figsize=(10, 3))
            if values["-plot1-"] == True :fig=plt.figure(figsize=(10, 3))
            if values["-plot3-"] == True :plt.figure(figsize=(5, 10))
            plt.rc('font', size=FONTSIZE)
        print(treename+':',shotastra,RUN)                
        if values["-list-"] == True :
            if name1 == 0:
                print('Choose name for sensor')
                continue
            VAR=np.array([])            
            var=np.array([])
            xname=np.array([])
            for shot in shots:
                print(shot)
                shotcalc=shotastra-shotst40+shot
                print(shotcalc)
                xname=np.append(xname,str(shot))
                if  values["-bprobes-"] == True: 
                    Y=b.read_bpprobe_exp(shot,name1,time1,time2)
                    TIME,var0=b.read_bpprobe_tree(treename,shotcalc,RUN)        
                    nt=np.where(TIME > time)[0][0]
                    var1=var0[nt,index]
                if  values["-floops-"] == True: 
                    Y=f.read_floop_exp(shot,name1,time1,time2)
                    TIME,var0=f.read_floop_tree(treename,shotcalc,RUN)
                    nt=np.where(TIME > time)[0][0]
                    var1=var0[nt,index]
                if  values["-rog-"] == True: 
                    print(shot,name1,time1,time2)
                    Y=rog.read_rog_exp_mean(shot,name1,time1,time2)
                    TIME,var0=rog.read_rog_tree(treename,name1,shotcalc,RUN)
                    nt=np.where(TIME > time)[0][0]
                    var1=var0[nt]
                VAR=np.append(VAR,Y)
                var=np.append(var,var1)
            if values["-overplot-"] == False :ax=fig.subplots()
            ax.plot(xname,VAR,label='exp-'+name1)
            ax.plot(xname,var,label='calc-'+name1)
            fig.autofmt_xdate(bottom=0.1, rotation=0, ha='center')
            plt.title(magname)
            legend=plt.legend(loc='upper left',fontsize='small') 
        else:
            if  values["-bprobes-"] == True:  
                TIME,var=b.read_bpprobe_tree(treename,shotastra,RUN)
                VAR=b.read_bpprobe_exp_all(shotst40,nameprobe,time1,time2)
                nt=np.where(TIME > time)[0][0]
                var1=var[nt,:nc]
            if  values["-floops-"] == True: 
                TIME,var=f.read_floop_tree(treename,shotastra,RUN)
                VAR=f.read_floop_exp_all(shotst40,nameloop,time1,time2)
                nt=np.where(TIME > time)[0][0]
                var1=var[nt,:nc]
            if  values["-rog-"] == True: 
                VAR=rog.read_rog_exp_all(shotst40,namerog,time1,time2)
                TIME,ROG,NAME=rog.read_rog_tree_all(treename,shotastra,RUN)
                ind=np.array([])
                for j in range(0,len(namerog)):
                    for i in range(0,len(NAME)):
                        if NAME[i] == 'ROG_'+namerog[j]: ind=np.append(ind,i)
                ind2=ind.astype(int)
                var=ROG[:,ind2]
                iupa=np.where(TIME > time2)
                iup=iupa[0][0]
                idwa=np.where(TIME < time1)
                idw=idwa[0][len(idwa[0])-1]
                var1=np.array([])
                for i in range(0,nc):
                    var1=np.append(var1,np.mean(var[idw:iup,i]))
            if values["-plot1-"] == True :
                if values["-overplot-"] == False :ax=fig.subplots()
                TIME_efit,CVALUE,MVALUE,SIGMA,WEIGHT,CHI,NAMEefit=efit.read_constraints(shotefit,magname,runE)
                ax.plot(name0,VAR,color='r',label='exp#'+str(shotst40)+', time='+str(time))
                ax.scatter(name0,VAR,s=WEIGHT[0,:]*facw,facecolors='none',edgecolors='r')
                ax.plot(name0,var1,label='calc#'+str(shotastra)+'@'+RUN+', time='+str(time))
                fig.autofmt_xdate(bottom=bottom, rotation=rotation, ha='center')
                plt.title(magname)
                legend=ax.legend(loc='upper left',fontsize='small')

            if values["-plot3-"] == True :
                VAR0=VAR-var1
                print(nt,TIME[nt],magname)
                Re,Ze,dre,dze,VARe=passives.read_EFIT_RZ(shotelmag)
                if  values["-bprobes-"] == True:
                    R,Z=b.read_RZ(shotst40)
                if  values["-floops-"] == True:
                    R,Z=f.read_RZ(shotst40)
                R1=R[:nc]
                Z1=Z[:nc]
                plt.scatter(Re,Ze,c='k',marker='.')                
                plt.scatter(R1,Z1,c=VAR0,s=30)
                for gx,gy,name1 in np.broadcast(R1,Z1,name0):
                    plt.annotate(name1,(gx,gy),xytext=(gx,gy))
                plt.jet()
                plt.colorbar(label="exp-calc: "+magname)
                plt.title(magname+'#'+str(shotst40)+'@'+RUN+' time='+str(TIME[nt]))
                legend=plt.legend(loc='upper left',fontsize='small')
        plt.show()

window.close()


