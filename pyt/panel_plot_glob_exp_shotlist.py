# python3 panel_plot_glob_exp_shotlist.py
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
import get23_data_shot_mean as get
import read_astra_globals as read
conn = Connection('192.168.1.7:8000')
LIST=[ 'WDIA','LI3M','BTPM','BTTM','BTOR','IPL','RGEO','CR0','NEL','TISX','TESX','RFX','HNBI','PNB','Te0TS','NETS','TImaxPI','VmaxPI','TImaxTWS','VmaxTWS']#
ASTRACALC=['FFAST','NeTiTauE','Ni0Ti0TauE','FCD','BTauE','BTauETOT','RHOSTAR','NUSTARE','NUSTARI','TauE_tot']
shotsGLOBUS=[11523,11525,11547,11548,11549,11552,11553,11576]
shotsIPL=[11224,11225,11226,11227,11228]# IPL=0.5MA 
shotsBT=[11211,11215,11224,11225,11229]#B=1.7T
shotsnTtau=[11380,11381,11382,11383,11384,11385,11386,11387,11388,11389]
shotsSS=[11416,11419,11420,11422]
shotsIPLD=[11424,11425,11426,11427,11428,11429]
shotsHotIon=[11030,11032,11472,11476,11478,11515,11517,11519]
shotsLH=[11570,11571,11573]
shotsalsu=[11147,11291,11292,11293,11294,11296,11297,11328,11333,11336,11337,11340,11341,11342,11354,11355,11358,11359,11361,11362,11364,11365,11376,11377,11379,11380,11381,11383,11384,11385,11415,11416,11417,11418,11419,11420,11421,11422,11424,11425,11426,11427,11428,11429,11436,11450,11469,11483,11515,11523,11547,11548,11549,11553,11555,11556,11557,11571,11574,11575,11576,11577,11581,11582]#RUN602
shotsBDA=[11089,11100,11211,11215,11224,11226,11227,11228,11237,11238,11312]#RUN610
shots=shotsGLOBUS
leng=11
var=np.array([])
combo_style={'size':(12,1)}
comboboxX=sg.InputCombo(values=[], **combo_style, enable_events=True, key='-COMBOX-')
comboboxY=sg.InputCombo(values=[], **combo_style, enable_events=True, key='-COMBOY-')
comboboxXC=sg.InputCombo(values=ASTRACALC, **combo_style, enable_events=True, key='-COMBOXC-')
comboboxYC=sg.InputCombo(values=ASTRACALC, **combo_style, enable_events=True, key='-COMBOYC-')
combobox2=sg.InputCombo(values=LIST, **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=LIST, **combo_style, enable_events=True, key='-COMBO3-')
oneshot=False
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
          [sg.T("time1="), sg.Input('0.07', size=(7,1), key="-time1-"),
           sg.T("time2="), sg.Input('0.08', size=(7,1), key="-time2-")],
          [sg.Radio('shotsnTtau', "RADIO0", default=False, key="-shotsnTtau-"),
           sg.Radio('shotsHotIon', "RADIO0", default=False, key="-shotsHotIon-"),
           sg.Radio('shotsSS', "RADIO0", default=False, key="-shotsSS-"),
           sg.Radio('shotsIPLD', "RADIO0", default=False, key="-shotsIPLD-")],
          [sg.Radio('shotsGLOBUS', "RADIO0", default=False, key="-shotsGLOBUS-"),
           sg.Radio('shotsLH', "RADIO0", default=False, key="-shotsLH-"),
           sg.Radio('shotsIPL', "RADIO0", default=False, key="-shotsIPL-"),
           sg.Radio('shotsBT', "RADIO0", default=False, key="-shotsBT-"),
           sg.Radio('shotsalsu', "RADIO0", default=False, key="-shotsalsu-")],
          [sg.Radio('shotsBDA', "RADIO0", default=False, key="-shotsBDA-")],
          [sg.Radio('Any shot', "RADIO0", default=True, key="-anyshot-"),
           sg.Input('11228', size=(8,1),key="-shot-")],
          [sg.Checkbox('Astra',default=True, key="-astra-")],
          [sg.T("ASTRA run"), sg.Input('602', size=(5,1), key="-run-"),sg.T("MDS+ range"), sg.Input('13000000', size=(8,1), key="-Range-"),sg.Button('read globnames',size=(10,1))],
          [sg.T("ASTRA global X")],
          [sg.Radio('Astra mds', "RADIO1",default=True, key="-astra_mdsX-"),comboboxX,sg.Radio('Astra calc', "RADIO1",default=False, key="-astra_calcX-"),comboboxXC],
          [sg.T("ASTRA global Y")],
          [sg.Radio('Astra mds', "RADIO2",default=True, key="-astra_mdsY-"),comboboxY,sg.Radio('Astra calc', "RADIO2",default=False, key="-astra_calcY-"),comboboxYC],

          [sg.Checkbox('Experiment',default=False, key="-experiment-")],
          [sg.T("Exp global X  "),combobox2,sg.T("Exp global Y  "),combobox3],
           
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

window = sg.Window('Plot exp & astra globals for shotlist', layout, size=(715, 600))
while True:
    event, values = window.read()
    Astra=False
    Exp=False
    mdsX=False
    mdsY=False
    time1=float(values["-time1-"])
    time2=float(values["-time2-"])
    if values['-astra-']==True:Astra=True
    if values['-astra_mdsX-']==True:mdsX=True
    if values['-astra_calcX-']==True:mdsX=False
    if values['-astra_mdsY-']==True:mdsY=True
    if values['-astra_calcY-']==True:mdsY=False
    if values['-experiment-']==True:Exp=True
#    if values['-anyshot-']==True:shot=values['-COMBO1-']
    if values['-shotsGLOBUS-']==True:shots=shotsGLOBUS
    if values['-shotsLH-']==True:shots=shotsLH
    if values['-shotsIPL-']==True:shots=shotsIPL
    if values['-shotsBT-']==True:shots=shotsBT
    if values['-shotsnTtau-']==True:shots=shotsnTtau
    if values['-shotsHotIon-']==True:shots=shotsHotIon
    if values['-shotsSS-']==True:shots=shotsSS
    if values['-shotsIPLD-']==True:shots=shotsIPLD
    if values['-shotsalsu-']==True:shots=shotsalsu
    if values['-shotsBDA-']==True:shots=shotsBDA
    if values['-anyshot-']==True:
        oneshot=True
        shots= [int(values['-shot-'])]
        print(shots)
    rang=int(values["-Range-"])
    RUN='RUN'+str(values["-run-"])
    if event == "read globnames":
        var=np.array([])
        g=Tree('astra',rang+shots[0]).getNode("\\TOP."+RUN+".GLOBAL").getNodeWild('*').getPath().data()
        num=g[0].decode().strip().find('GLOBAL') 
        for i in range(0,len(g)):
            el=g[i].decode().strip()[num+7:num+7+leng] 
            print(el)
            if(el != 'HELP'):var = np.append(var,el)
        variables=var.tolist()
        comboboxX.Update(values=variables)
        comboboxY.Update(values=variables)
    if event == '-COMBOX-' :
        globnameX= values['-COMBOX-']
        conn.openTree('astra',rang+shots[0])
        print(RUN+'.GLOBAL.'+globnameX+':HELP')
        text=conn.get(RUN+'.GLOBAL.'+globnameX+':HELP')
        print(globnameX+':')
        print(text)
    if event == '-COMBOXC-' :
        globnameX= values['-COMBOXC-']
        conn.openTree('astra',rang+shots[0])
        print('reading '+globnameX)
    if event == '-COMBOY-' :
        globnameY= values['-COMBOY-']
        conn.openTree('astra',rang+shots[0])
        print(RUN+'.GLOBAL.'+globnameY+':HELP')
        text=conn.get(RUN+'.GLOBAL.'+globnameY+':HELP')
        print(globnameY+':')
        print(text)
    if event == '-COMBOYC-' :
        globnameY= values['-COMBOYC-']
        conn.openTree('astra',rang+shots[0])
        print('reading '+globnameY)
    if event == '-COMBO2-' :
        globnameXexp= values['-COMBO2-']
        print(globnameXexp)
    if event == '-COMBO3-' :
        globnameYexp= values['-COMBO3-']
        print(globnameYexp)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    if event== "make plot":
        if Astra:
            print('Astra  case')
            print(shots,globnameX,globnameY)
            read.plot_globXY(shots,rang,RUN,globnameX,mdsX,globnameY,mdsY,time1,time2)
            plt.suptitle('ASTRA@'+str(RUN)+' '+str(time1)+'<t<'+str(time2))
            plt.xlabel(globnameX)        
            plt.ylabel(globnameY)        
        if Exp:
            if oneshot == True :print(shots,globnameXexp,globnameYexp)
            print(globnameXexp,globnameYexp)
            get.plot_exp(shots,globnameXexp,globnameYexp,time1,time2)
            plt.suptitle(str(time1)+'<t<'+str(time2))
            plt.xlabel(globnameXexp)        
            plt.ylabel(globnameYexp)        

        plt.legend(loc='upper left',fontsize='small')
    plt.show()
window.close()


