# python3 pyt/panel_plot_glob.py
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
import read_astra_globals as read
import read_transp as transp
import read_efit as efit
efitglobal=False;    efitvirial=False
conn = Connection('192.168.1.7:8000')
shotastra=13011228
r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',shotastra).getNode("\\TOP.RUN613.GLOBAL").getNodeWild('*').getPath().data()
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
ASTRACALC=['TEA','NEA','TIA','LIMACT','X-points','TAUGLOB','Tau20','H20','PLH','PTOT_ABS','FULLNEUT','SH_AS','FFAST','NeTiTauE','Ni0Ti0TauE','FCD','BTauE','BTauETOT','RHOSTAR','NUSTARE','NUSTARI','TauE_tot']
names=ASTRACALC
key='read'
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=names, **combo_style, enable_events=True, key='-COMBO3-')
combobox4=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO4-')
combobox5=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO5-')
combobox6=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO6-')
FONTSIZE=12 
plt.figure(figsize=(10, 3))
plt.rc('font', size=FONTSIZE)
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))],
          [sg.Checkbox('ASTRA',default=True, key="-astra-"),
           sg.T("ASTRA shot="), sg.Input('13011228', size=(8,1),key="-shot-"),
           sg.Button('reread shot',size=(10,1))],
          [sg.T("RUN"),combobox1,sg.Button('reread ASTRA names',size=(20,1)),
           sg.Button('HELPrun',size=(10,1))],
          [sg.T("Globals"),combobox2,sg.Button('HELPglob',size=(10,1))],
          [sg.T("Calc globals"),combobox3],
          [sg.Checkbox('TRANSP',default=False, key="-transp-"),
           sg.T("TRANSP shot="), sg.Input('34011560', size=(8,1),key="-shotT-"),
           sg.T("TRANSP run"), sg.Input('T06', size=(5,1), key="-runT-"),
           sg.Button('reread TRANSP names',size=(20,1))],
          [sg.T("TRANSP Globals"),combobox4],
          [sg.Checkbox('EFIT',default=False, key="-efit-"),
           sg.T("EFIT shot="), sg.Input('13311419', size=(8,1),key="-shotE-"),
           sg.T("EFIT run"), sg.Input('RUN2340', size=(5,1), key="-runE-"),
           sg.Button('reread EFIT names',size=(20,1))],
          [sg.T("EFIT Globals"),combobox5],
          [sg.T("EFIT Virials"),combobox6],
          [sg.Checkbox('new figure',default=False, key="-newfig-")],
          [sg.T("")]]

window = sg.Window('Plot globals', layout, size=(715, 500))
while True:
    event, values = window.read()
    shotastra=int(values["-shot-"])
    shottransp=int(values["-shotT-"])
    shotefit=int(values["-shotE-"])
    runT=values["-runT-"]
    runE=values["-runE-"]
    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el)
            try:
                if el[3] !='0':run = np.append(run,el)
            except: pass
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print(key,'Comment for '+RUN+':')
        print(text)
    if event == '-COMBO2-' :
        glob= values['-COMBO2-']
        conn.openTree('astra',shotastra)
        print(key,RUN+'.GLOBAL.'+glob+':HELP')
        text=conn.get(RUN+'.GLOBAL.'+glob+':HELP')
        print(glob+':')
        print(text)
    if event == '-COMBO3-' :
        glob=values['-COMBO3-']
        key='calc'
        print(key,glob)
        conn.openTree('astra',shotastra)
    if event == "reread ASTRA names":
        var=np.array([])
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".GLOBAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('GLOBAL') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+7:num+7+leng] 
            print(el)
            if(el != 'HELP'):var = np.append(var,el)
        variables=var.tolist()
        combobox2.Update(values=variables)
    if event == '-COMBO4-' : globT= values['-COMBO4-']
    if event == "reread TRANSP names":
        var=np.array([])
        g=Tree('TRANSP_TEST',shottransp).getNode("\\TOP."+runT+".GLOBAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('.GLOBAL') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+8:]#num+8+leng] 
            print(el)
            var = np.append(var,el)
        variables=var.tolist()
        combobox4.Update(values=variables)
    if event == '-COMBO5-' : 
        globE= values['-COMBO5-']
        efitglobal=True
    if event == '-COMBO6-' : 
        globE= values['-COMBO6-']
        efitvirial=True
    if event == "reread EFIT names":
        var=np.array([])
        g=Tree('EFIT',shotefit).getNode("\\TOP."+runE+".GLOBAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('.GLOBAL') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+8:]#num+8+leng] 
            print(el)
            var = np.append(var,el)
        variables=var.tolist()
        combobox5.Update(values=variables)
        var=np.array([])
        g=Tree('EFIT',shotefit).getNode("\\TOP."+runE+".VIRIAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('.VIRIAL') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+8:]#num+8+leng] 
            print(el)
            var = np.append(var,el)
        variables=var.tolist()
        combobox6.Update(values=variables)
    if event == "HELPrun":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()
        for i in range(0,len(r)):
            run=r[i][12:20].decode().strip()
            print(run+':HELP')
            if(run != 'HELP'):
                text=conn.get(run+':HELP')
                print(run+': ',text)
    if event == "HELPglob":
        g=Tree('astra',shotastra).getNode("\\TOP."+RUN+".GLOBAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('GLOBAL') 
        conn.openTree('astra',shotastra)
        for i in range(0,len(g)):
            glob=g[i].decode().strip()[num+7:num+7+leng] 
            print(RUN+'.GLOBAL.'+glob+':HELP')
            if(glob != 'HELP'):
                text=conn.get(RUN+'.GLOBAL.'+glob+':HELP')
                print(glob+': ',text)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        if values["-newfig-"] == True : 
            plt.figure(figsize=(10, 3))
            plt.rc('font', size=FONTSIZE)
        if values["-astra-"] == True : 
            print('ASTRA:',shotastra,RUN,glob)
            if key == 'read':
                TIME,VAR=read.read_global(shotastra,glob,RUN)
            if key == 'calc':
                TIME,VAR=read.calc_global(shotastra,glob,RUN)
                key='read'
        if values["-transp-"] == True : 
            print('TRANSP:',shottransp,runT,globT)
            TIME,VAR=transp.read_glob(shottransp,globT,runT)
            try:
                TIME[0]
                plt.plot(TIME,VAR,label=globT+'-'+str(shottransp)+'@'+runT)
            except:print('TRANSP: check',shottransp,globT,runT)
        if values["-efit-"] == True : 
            print('EFIT:',shotefit,runE,globE)
            print(efitglobal,efitvirial)
            if efitglobal: TIME,VAR=efit.read_global(shotefit,globE,runE)
            if efitvirial: TIME,VAR=efit.read_virial(shotefit,globE,runE)
            try:
                TIME[0]
                plt.plot(TIME[1:],VAR[1:],label=globE+'-'+str(shotefit)+'@'+runE)
            except:print('EFIT: check',shotefit,globE,runE)
        try:
            TIME.bit_length()
        except:
            legend=plt.legend(loc='upper left',fontsize='small')
            plt.show()




window.close()


