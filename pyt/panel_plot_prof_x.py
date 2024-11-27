# python3 pyt/panel_plot_prof_x.py
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
import plot_run_prof_fill as read
import read_transp as transp
conn = Connection('192.168.1.7:8000')
r=Tree('astra',13011228).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',13011228).getNode("\\TOP.RUN613.PROFILES.ASTRA").getNodeWild('*').getPath().data()
run=np.array([])
ASTRACALC=['DVOL','PRESSE','PRESSTH']
TRANSPCALC=['VOL']
key='read'
keyT='read'
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    #print(el) 
    run = np.append(run,el)

runs=run.tolist()
leng=12
var=np.array([])
num=g[0].decode().strip().find('S.ASTRA') 
for i in range(0,len(g)-1):
    el=g[i].decode().strip()[num+8:num+8+leng] 
    #print(el) 
    if(el != 'HELP'):var = np.append(var,el)

variables=var.tolist()
combo_style={'size':(12,1)}
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO3-')
combobox4=sg.InputCombo(values=ASTRACALC, **combo_style, enable_events=True, key='-COMBO4-')
combobox5=sg.InputCombo(values=TRANSPCALC, **combo_style, enable_events=True, key='-COMBO5-')
plt.figure()
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),sg.T("        "),
           sg.Button('Exit',size=(4,2))], 
          [sg.Checkbox('ASTRA',default=True, key="-astra-"),
           sg.T("ASTRA shot="), sg.Input('13011228', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1,sg.Button('reread ASTRA names',size=(20,1)),
           sg.Button('HELPrun',size=(10,1))],
          [sg.T("Profiles"),combobox2,sg.Button('HELP prof',size=(12,1))],
          [sg.T("Calc profiles"),combobox4],
          [sg.Checkbox('TRANSP',default=False, key="-transp-"),
           sg.T("TRANSP shot="), sg.Input('34011560', size=(8,1),key="-shotT-"),
           sg.T("TRANSP run"), sg.Input('T06', size=(5,1), key="-runT-"),
           sg.Button('reread TRANSP names',size=(20,1))],
          [sg.T("TRANSP Profiles"),combobox3],
          [sg.T("Calc profiles"),combobox5],
          [sg.T("time1="), sg.Input('0.07', size=(7,1), key="-time1-"),
           sg.T("time2="), sg.Input('0.08', size=(7,1), key="-time2-")],
          [sg.Radio('RHOTOR', "RADIO1",default=True, key="-RHO-"),
           sg.Radio('RMID', "RADIO1",default=False, key="-R-")],
          [sg.Checkbox('new figure',default=False, key="-newfig-")]]
        

window = sg.Window('Plot profiles', layout, size=(715, 500))
while True:
    event, values = window.read()
    shotastra=int(values["-shot-"])
    shottransp=int(values["-shotT-"])
    runT=values["-runT-"]
    time1=float(values["-time1-"])
    time2=float(values["-time2-"])
    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el) 
            if el[3] !='0':run = np.append(run,el)
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
        conn.closeTree
    if event == '-COMBO2-' :
        profA= values['-COMBO2-']
        conn.openTree('astra',shotastra)
        print(RUN+'.PROFILES.ASTRA.'+profA+':HELP')
        text=conn.get(RUN+'.PROFILES.ASTRA.'+profA+':HELP')
        print(profA+':')
        print(text)
        conn.closeTree
    if event == '-COMBO4-' :
        profA=values['-COMBO4-']
        key='calc'
    if event == "reread ASTRA names":
        var=np.array([])
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".PROFILES.ASTRA").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.ASTRA') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+8:num+8+leng] 
            print(el)
            if(el != 'HELP'):var = np.append(var,el)
        variables=var.tolist()
        combobox2.Update(values=variables)
    if event == '-COMBO3-' : profT= values['-COMBO3-']
    if event == '-COMBO5-' :
        profT=values['-COMBO5-']
        keyT='calc'
    if event == "reread TRANSP names":
        var=np.array([])
        g=Tree('TRANSP_TEST',shottransp).getNode("\\TOP."+runT+".PROFILES.RHOTOR").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.RHOTOR') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+9:]#num+8+leng] 
            print(el)
            var = np.append(var,el)
        variables=var.tolist()
        combobox3.Update(values=variables)
    if event == "HELPrun":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()
        for i in range(0,len(r)):
            run=r[i][12:20].decode().strip()
            print(run+':HELP')
            if(run != 'HELP'):
                text=conn.get(run+':HELP')
                print(run+': ',text)
    if event == "HELP prof":
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".PROFILES.ASTRA").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('S.ASTRA') 
        conn.openTree('astra',shotastra)
        for i in range(0,len(g)):
            profA=g[i].decode().strip()[num+8:num+8+leng] 
            print(RUN+'.PROFILES.ASTRA.'+profA+':HELP')
            if(profA != 'HELP'):
                text=conn.get(RUN+'.PROFILES.ASTRA.'+profA+':HELP')
                print(profA+': ',text)
        conn.closeTree
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":

        if values["-newfig-"] == True : plt.figure()
        if values["-astra-"] == True : 
            print('ASTRA:',shotastra,RUN,profA)
            if  values["-RHO-"] == True :
                if key == 'read':
                    XN,VAR1,VAR2,VARMIN,VARMAX=read.read_prof_rho(shotastra,profA,RUN,time1,time2)
                if key == 'calc':
                    XN,VAR1,VAR2,VARMIN,VARMAX=read.read_calc_rho(shotastra,profA,RUN,time1,time2)
                    key='read'
                try:
                    XN[0]
                    print(len(XN),len(VAR1))
                    plt.fill_between(XN,VARMIN,VARMAX,color='red',alpha=0.2)
                    plt.plot(XN,VAR1,label=profA+'-'+str(shotastra)+'@'+RUN+';t='+str(time1))
                    plt.plot(XN,VAR2,label=profA+'-'+str(shotastra)+'@'+RUN+';t='+str(time2))
                    plt.xlabel('rho_tor',fontsize=15)
                except:print('ASTRA: check',shotastra,profA,RUN,time1,time2)

            if  values["-R-"] == True :
                R1,R2,VAR1,VAR2=read.read_prof_R(shotastra,profA,RUN,time1,time2)
                try:
                    R1[0]
                    plt.plot(R1,VAR1,label=profA+'-'+str(shotastra)+'@'+RUN+';t='+str(time1)) 
                    plt.plot(R2,VAR2,label=profA+'-'+str(shotastra)+'@'+RUN+';t='+str(time2)) 
                    plt.xlabel('major radius, m',fontsize=15)
                except:print('ASTRA: check',shotastra,profA,RUN,time1,time2)
        if values["-transp-"] == True : 
            print('TRANSP:',shottransp,runT,profT)
            if  values["-RHO-"] == True :
                if keyT == 'read':
                    XN,VAR1,VAR2,VARMIN,VARMAX=transp.read_prof_rho(shottransp,profT,runT,time1,time2)
                if keyT == 'calc':
                    XN,VAR1,VAR2,VARMIN,VARMAX=transp.read_calc_rho(shottransp,profT,runT,time1,time2)
                    keyT='read'
                try:
                    XN[0]
                    plt.fill_between(XN,VARMIN,VARMAX,color='red',alpha=0.2)
                    plt.plot(XN,VAR1,label=profT+'-'+str(shottransp)+'@'+runT+';t='+str(time1))
                    plt.plot(XN,VAR2,label=profT+'-'+str(shottransp)+'@'+runT+';t='+str(time2))
                    plt.xlabel('rho_tor',fontsize=15)
                except:print('TRANSP: check',shottransp,profT,runT,time1,time2)
            if  values["-R-"] == True :
                R1,R2,VAR1,VAR2=transp.read_prof_R(shottransp,profT,runT,time1,time2)
                try:
                    R1[0]
                    plt.plot(R1,VAR1,label=profT+'-'+str(shottransp)+'@'+runT+';t='+str(time1)) 
                    plt.plot(R2,VAR2,label=profT+'-'+str(shottransp)+'@'+runT+';t='+str(time2)) 
                    plt.xlabel('major radius, m',fontsize=15)
                except:print('TRANSP: check',shottransp,profT,runT,time1,time2)
        plt.suptitle(str(time1)+'<t<'+str(time2))
        legend=plt.legend(loc='upper right',fontsize='small')
        plt.show()
window.close()


