# python3 pyt/panel_coilcurrents.py
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import coilcurrents_functions as c
import rog_functions as rog
PSUASTRA=['DIV','BVL','BVUT','BVUB','CS','MC','MCT','MCB','PSH']
PSUST40=['DIV','BVL','BVUT','BVUB','SOL','MC','PSH']
count=0;count1=0
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.Button('Exit',size=(4,2))],
          [sg.T("")],
          [sg.Checkbox('',default=True, key="-exp-"),
           sg.T("ST40 shot ="), sg.Input('11419', size=(6,1),key="-SHOT-")],
          [sg.Checkbox('Plasma',default=False, key="-plasma-"),
           sg.Checkbox('Vacuum',default=False, key="-vacuum-")],
          [sg.T("What tree?"), 
           sg.Radio('ASTRA', "RADIO2", default=True, key="-astra-"),
           sg.Radio('SPIDER', "RADIO2", default=False, key="-spider-")],
          [sg.T("ASTRA shot="), sg.Input('13000025', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"), sg.Input('105', size=(5,1), key="-run-")],
          [sg.Checkbox('DIV',default=True, key="-DIV-"),
           sg.Checkbox('DIVBWIRE',default=False, key="-DIVBWIRE-"),
           sg.Checkbox('DIVTWIRE',default=False, key="-DIVTWIRE-")],
          [sg.Checkbox('BVL',default=True, key="-BVL-"),      
           sg.Checkbox('BVLWIRE',default=False, key="-BVLWIRE-")],
          [sg.Checkbox('BVUB',default=True, key="-BVUB-"),
           sg.Checkbox('BVUBWIRE',default=False, key="-BVUBWIRE-")],
          [sg.Checkbox('BVUT',default=True, key="-BVUT-"),
           sg.Checkbox('BVUTWIRE',default=False, key="-BVUTWIRE-")],
          [sg.Checkbox('SOL',default=True, key="-SOL-"),
           sg.Checkbox('SOLWIRE',default=False, key="-SOLWIRE-")],
          [sg.Checkbox('MC',default=False, key="-MC0-"),
           sg.Radio('MC',"RADIO1",default=True, key="-MC-"),sg.T(" #13011615 only: "),
           sg.Radio('MCT',"RADIO1",default=False, key="-MCT-"),
           sg.Radio('MCB',"RADIO1",default=False, key="-MCB-")],
          [sg.Checkbox('MCWIRE',default=False, key="-MCWIRE-")],
          [sg.Checkbox('PSH',default=False, key="-PSH-"),
           sg.Checkbox('PSHBWIRE',default=False, key="-PSHBWIRE-"),
           sg.Checkbox('PSHTWIRE',default=False, key="-PSHTWIRE-")],
          [sg.Checkbox('IPL',default=False, key="-IPL-")],
          [sg.Checkbox('TF',default=False, key="-TF-")],
          [sg.T("")],[sg.T("")]]

    #[sg.Checkbox('',default=True, key="--")],


###Setting Window
window = sg.Window('coil currents and Ipl', layout, size=(600,600),keep_on_top=False)

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    shots=np.array([])
    shotst40=int(values["-SHOT-"])
    shots=np.append(shots,shotst40)
    shotastra=int(values["-shot-"])
    runnumber=int(values["-run-"])
    RUNv='RUN0'+str(runnumber)
    RUNp='RUN'+str(runnumber)
    index=np.array([])
    if values["-astra-"]== True : treename='astra'
    if values["-spider-"]== True : treename='spider'
    if values["-DIV-"]== True : index=np.append(index,1)
    if values["-BVL-"]== True : index=np.append(index,2)
    if values["-BVUT-"]== True : index=np.append(index,3)
    if values["-BVUB-"]== True : index=np.append(index,4)
    if values["-SOL-"]== True : index=np.append(index,5)
    if values["-MC0-"]== True :         
        if values["-MC-"]== True : index=np.append(index,6)
        if values["-MCT-"]== True : index=np.append(index,7)
        if values["-MCB-"]== True : index=np.append(index,8)
    if values["-PSH-"]== True : index=np.append(index,9)
    if values["-TF-"]== True : index=np.append(index,10)
    indwire=np.array([])    
    if values["-MCWIRE-"]== True : indwire=np.append(indwire,14)
    if values["-DIVBWIRE-"]== True : indwire=np.append(indwire,15)
    if values["-DIVTWIRE-"]== True : indwire=np.append(indwire,17)
    if values["-BVLWIRE-"]== True : indwire=np.append(indwire,16)
    if values["-SOLWIRE-"]== True : indwire=np.append(indwire,18)
    if values["-BVUBWIRE-"]== True : indwire=np.append(indwire,19)
    if values["-BVUTWIRE-"]== True : indwire=np.append(indwire,20)
    if values["-PSHBWIRE-"]== True : indwire=np.append(indwire,21)
    if values["-PSHTWIRE-"]== True : indwire=np.append(indwire,22)

    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        ind=index.astype(int)
        indastra=np.extract(ind!=10,ind)
        names=np.array([])
        for j in range(len(indastra)):
            names=np.append(names,PSUASTRA[indastra[j]-1])
        t1=0.5;t2=-1;t3=0.5;t4=-1
        #count=0
        if values["-exp-"]== True and treename == 'astra': 
            if values["-vacuum-"]== True : 
                t1,t2=c.astra_t1_t2(shotastra,RUNv)
            tmin=min(t1,t2)
            if values["-plasma-"]== True :
                t1,t1=c.astra_t1_t2(shotastra,RUNp)
            tmax=max(t1,t2)
            print(tmin,tmax)
            count1=c.plot_coilcurrents_exp(shotst40,ind,tmin,tmax,count)
            count=count1
            if values["-IPL-"]== True :
                c.plot_ipl_exp(shotst40)  
            if len(indwire)>0 :
                ind1=indwire.astype(int)
                rog.plot_rog_exp(ind1,shots,False)
 
        if values["-vacuum-"]== True : 
            count1=c.plot_coilcurrents_astra(treename,shotastra,RUNv,indastra,count)
            if count1 == -1:
                count1=c.plot_coilcurrents_astra_all(treename,shotastra,RUNv,names,count)
            if values["-IPL-"]== True :
                c.plot_ipl_astra(treename,shotastra,RUNv)
        if values["-plasma-"]== True : 
            count1=c.plot_coilcurrents_astra(treename,shotastra,RUNp,indastra,count)
            if count1 == -1:
                count1=c.plot_coilcurrents_astra_all(treename,shotastra,RUNp,names,count)
            count=count1
            if values["-IPL-"]== True :
                c.plot_ipl_astra(treename,shotastra,RUNp)
        plt.legend(loc='upper right',fontsize='small')
        #plt.xlim(0,0.25)
        plt.show()


window.close()

