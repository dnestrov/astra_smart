# python3 pyt/panel_chi2.py
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
from scipy import interpolate

conn = Connection('192.168.1.7:8000')
shotastra=13012050
RUN='RUN201'
shotefit=12050
runE='BEST'
shotelmag=206
r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',shotastra).getNode("\\TOP.RUN201.GLOBAL").getNodeWild('*').getPath().data()
run=np.array([])
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    print(el) 
    run = np.append(run,el)

runs=run.tolist()
leng=11
var=np.array([])
num=g[0].decode().strip().find('GLOBAL') 
for i in range(0,len(g)-1):
    el=g[i].decode().strip()[num+7:num+7+leng] 
    #print(el) 
    if(el != 'HELP'):var = np.append(var,el)

variables=var.tolist()
combo_style={'size':(12,1)}

combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
FONTSIZE=12
treename='ASTRA'
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))],
          [sg.Checkbox('Calc',default=True, key="-calc-"),
           sg.Radio('ASTRA', "RADIO1",default=True, key="-astra-"),
           sg.Radio('SPIDER', "RADIO1",default=False, key="-spider-"),
           sg.T("ASTRA shot="), sg.Input('13012050', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1,
           sg.Button('HELPrun',size=(10,1))],
          [sg.Checkbox('BPPROBES',default=True, key="-bprobes-"),
           sg.Checkbox('FL_LOOPS',default=False, key="-floops-"),
           sg.Checkbox('ROG',default=False, key="-rog-")],
          [sg.Checkbox('EFIT',default=False, key="-efit-"),
           sg.T("EFIT shot="), sg.Input('12050', size=(8,1),key="-shotE-"),
           sg.T("EFIT run"), sg.Input('BEST', size=(8,1), key="-runE-")],
          [sg.Checkbox('plot over sensor',default=False, key="-plot1-"),
           sg.T("time="), sg.Input('0.07', size=(7,1), key="-time-"),],
          [sg.Checkbox('plot over time',default=False, key="-plot2-")],
          [sg.Checkbox('plot R,Z',default=False, key="-plot3-")],
          [sg.Checkbox('overplot',default=False, key="-overplot-")],
          [sg.T("")]]

window = sg.Window('chi^2 ASTRA vs EFIT', layout, size=(715, 500))
while True:
    plt.rc('font', size=FONTSIZE)
    event, values = window.read()
    shotastra=int(values["-shot-"])
    shotefit=int(values["-shotE-"])
    runE=values["-runE-"]
    time=float(values["-time-"])
    if values["-astra-"]== True : treename='ASTRA'
    if values["-spider-"]== True : treename='SPIDER'
    n1=13
    if treename == "ASTRA": n1=12
    if event == "reread shot":
        r=Tree(treename,shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][n1:20].decode().strip()
            print(el)
            try:
                if el[3] !='0':run = np.append(run,el)
            except: pass
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree(treename,shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
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
            if values["-plot1-"] == True :plt.figure(figsize=(10, 3))
            if values["-plot2-"] == True :plt.figure(figsize=(10, 3))
            if values["-plot3-"] == True :plt.figure(figsize=(5, 10))
            plt.rc('font', size=FONTSIZE)
        print(treename+':',shotastra,RUN)
        if values["-calc-"] == True: 
            if  values["-bprobes-"] == True:  
                magname='BP'
                num=10
                TIME,var=b.read_bpprobe_tree(treename,shotastra,RUN)
            if  values["-floops-"] == True: 
                magname='FLUX'
                num=10
                TIME,var=f.read_floop_tree(treename,shotastra,RUN)
                var=var/2/math.pi
            if  values["-rog-"] == True: 
                magname='ROGC'
                TIME,var=rog.read_rogefit_tree(treename,shotastra,RUN)
            TIME_efit,CVALUE,MVALUE,SIGMA,WEIGHT,CHI,NAME=efit.read_constraints(shotefit,magname,runE)
            nc=len(MVALUE[0,:])
            nt=np.where(TIME_efit > time)[0][0]
            #getting only data used in EFIT :
            var1=var[1:,:nc] 
            TIME1=TIME[1:]
            chi2=0*TIME_efit
            chi2n=np.array([])
            chi2w=np.array([])
            print(nt,TIME_efit[nt],magname)
            name0=np.array([])
            for i in range(nc):
                name0=np.append(name0,NAME[i].strip()[num:])
                ftime=interpolate.InterpolatedUnivariateSpline(TIME1,var1[:,i],k=3)
                var2=ftime(TIME_efit)
                chi2n=np.append(chi2n,             ((var2[nt]-MVALUE[nt,i])/SIGMA[nt,i])**2)
                chi2w=np.append(chi2w,(WEIGHT[nt,i]*(var2[nt]-MVALUE[nt,i])/SIGMA[nt,i])**2)
                chi2=chi2+(WEIGHT[:,i]*(var2-MVALUE[:,i])/SIGMA[:,i])**2
                print(NAME[i].strip(),WEIGHT[nt,i],SIGMA[nt,i],(WEIGHT[nt,i]*(var2[nt]-MVALUE[nt,i])/SIGMA[nt,i])**2,chi2[nt])
            if values["-plot1-"] == True :
                plt.plot(chi2n,label='CHI2-'+treename+'-'+magname+', time='+str(TIME_efit[nt])+' WEIGTH=1')
                plt.plot(chi2w,label='CHI2-'+treename+'-'+magname+', time='+str(TIME_efit[nt]))
                

            if values["-plot2-"] == True : 
                plt.plot(TIME_efit,chi2,label='CHI2-'+treename+'-'+magname+'#'+str(shotastra)+'@'+str(RUN))
                plt.ylim(ymin=0,ymax=np.mean(chi2))
            if values["-plot3-"] == True :
                Re,Ze,dre,dze,VAR=passives.read_EFIT_RZ(shotelmag)
                if  values["-bprobes-"] == True:
                    R,Z=b.read_RZ(shotefit)
                if  values["-floops-"] == True:
                    R,Z=f.read_RZ(shotefit)
                R1=R[:nc]
                Z1=Z[:nc]
                plt.scatter(Re,Ze,c='k',marker='.')                
                plt.scatter(R1,Z1,c=chi2w,s=WEIGHT[nt,:]/SIGMA[nt,:]+10)
                for gx,gy,name in np.broadcast(R1,Z1,name0):
                    plt.annotate(name,(gx,gy),xytext=(gx,gy))
                plt.jet()
                plt.colorbar(label=magname+" values")
                plt.title(treename+'-'+magname+'#'+str(shotastra)+' time='+str(TIME_efit[nt]))
        if values["-efit-"] == True : 
            print('EFIT:',shotefit,runE)            
            if  values["-bprobes-"] == True:  magname='BP';num=10
            if  values["-floops-"] == True: magname='FLUX';num=10
            if  values["-rog-"] == True: magname='ROGC'
            TIME_efit,CVALUE,MVALUE,SIGMA,WEIGHT,CHI,NAME=efit.read_constraints(shotefit,magname,runE)
            nc=len(CHI[0,:])
            nt=np.where(TIME_efit > time)[0][0]
            CHI2_efit=np.sum(CHI,axis=1)
            name0=np.array([])
            for i in range(nc):
                name0=np.append(name0,NAME[i].strip()[num:])
                print(NAME[i].strip(),WEIGHT[nt,i],SIGMA[nt,i],CHI[nt,i])
            if values["-plot1-"] == True :
                plt.plot(CHI[nt,:],label='CHi2-EFIT-'+magname+' time='+str(TIME_efit[nt]))
                #plt.plot((WEIGHT[nt,:]*(CVALUE[nt,:]-MVALUE[nt,:])/SIGMA[nt,:])**2,label='EFIT-formula')
            if values["-plot2-"] == True :
                plt.plot(TIME_efit,CHI2_efit,label='CHI2-EFIT-'+magname+'#'+str(shotefit)+'@'+str(runE))
            if values["-plot3-"] == True :
                Re,Ze,dre,dze,VAR=passives.read_EFIT_RZ(shotelmag)
                if  values["-bprobes-"] == True:
                    R,Z=b.read_RZ(shotefit)
                if  values["-floops-"] == True:
                    R,Z=f.read_RZ(shotefit)
                R1=R[:nc]
                Z1=Z[:nc]
                plt.scatter(Re,Ze,c='k',marker='.')                
                plt.scatter(R1,Z1,c=CHI[nt,:],s=WEIGHT[nt,:]/SIGMA[nt,:]+10)
                for gx,gy,name in np.broadcast(R1,Z1,name0):
                    plt.annotate(name,(gx,gy),xytext=(gx,gy))
                plt.jet()
                plt.colorbar(label=magname+" values")
                plt.title('EFIT-'+magname+'#'+str(shotefit)+'@'+runE+' time='+str(TIME_efit[nt]))
         
        legend=plt.legend(loc='upper left',fontsize='small')
        plt.show()




window.close()


