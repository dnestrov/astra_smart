# python3 pyt/panel_plot_glob_exp.py
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
import get23_data_shot_time as get
#conn = Connection('192.168.1.7:8000')

LIST=[ 'WDIAEF','LI3MEF','BTPMEF','BTTMEF','BTOREF','IPL','RGEOEF','IN_EF','OUT_EF','SH_EF','RMAGEF','AMINEF','NEL','TISX','TESX','RFX','HNBI','PNB','Te0TS','Ne0TS','RMAGTS','IN_TS','OUT_TS','SH_TS','TImaxPI','VmaxPI','TImaxTWS','VmaxTWS']
shotsGLOBUS=[11523,11525,11547,11548,11549,11552,11553,11576]
shotsIPL=[11224,11225,11226,11227,11228]# IPL=0.5MA 
shotsBT=[11211,11215,11224,11225,11229]#B=1.7T
shotsnTtau=[11380,11381,11382,11383,11384,11385,11386,11387,11388,11389]
shotsSS=[11416,11419,11420,11422]
shotsIPLD=[11424,11425,11426,11427,11428,11429]
shotsHotIon=[11030,11032,11472,11476,11478,11515,11517,11519]
shotsLH=[11570,11571,11573]
shotsalsu=[11147,11291,11292,11293,11294,11296,11297,11328,11333,11336,11337,11340,11341,11342,11354,11355,11358,11359,11361,1136,11364,11365,11376,11377,11379,11380,11381,11383,11384,11385,11415,11416,11417,11418,11419,11420,11421,11422,11424,11425,11426,11427,11428,11429,11436,11450,11469,11483,11515,11523,11547,1154,11549,11553,11555,11556,11557,11571,11574,11575,11576,11577,11581,11582]#RUN602
shotsBDA=[11089,11100,11211,11215,11224,11226,11227,11228,11237,11238,11312]#RUN610
shots=shotsGLOBUS
combo_style={'size':(12,1)}
combobox1=sg.InputCombo(values=shots, **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=LIST, **combo_style, enable_events=True, key='-COMBO2-')
oneshot=False
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
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
          [sg.T("SHOTS"),combobox1,sg.Button('reread shots',size=(10,1))],
          [sg.Radio('Any shot', "RADIO0", default=True, key="-anyshot-"),
           sg.Input('11228', size=(8,1),key="-shot-")],
          [sg.T("Exp data"),combobox2],
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

window = sg.Window('Plot exp variables in time', layout, size=(715, 500))
while True:
    event, values = window.read()
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
    if values['-anyshot-']==False:
        if event == "reread shots" :
            combobox1.Update(values=shots)            
    else:
        oneshot=True
        shot= int(values['-shot-'])
        print(shot)
    if event == '-COMBO1-' :
        shot= values['-COMBO1-']
        print(shot)
    if event == '-COMBO2-' :
        globname= values['-COMBO2-']
        print(globname)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    if event== "make plot":
        if oneshot == True :print(shot,globname)
        err=''

        if globname == 'NEL':
            err,TIME,glob=get.get_smm_data(shot)
            print(err,TIME)
        if globname[len(globname)-2:len(globname)] == 'TS':
            err,TIME,glob=get.get_TS_1Ddata(shot,globname)
            print(err,TIME)
        if globname[len(globname)-2:len(globname)] == 'EF':
            err,TIME,glob=get.get_EFIT_global(shot,globname,'BEST')
            print(err,TIME)
        if globname == 'IPL':
            err,TIME,glob=get.get_IPL_pfit(shot)
            print(err,TIME)
        if globname == 'RFX' or globname == 'HNBI':
            err,TIME,glob,dummy,dummy=get.get_NBI_data(shot,globname)
            print(err,TIME,glob)
        if globname == 'PNB':
            err,TIME1,glob1,TIME2,glob2=get.get_NBI_data(shot,globname)
        if globname == 'TISX' or globname == 'TESX':
            err,TIME,glob,globerr=get.get_XRCS_data(shot,globname)
            print(err,TIME,glob)
        if globname == 'TImaxTWS' or globname == 'VmaxTWS':
            err,TIME,glob,globerr=get.get_TWS_data(shot,globname)
            print(err,TIME,glob)
        if globname == 'TImaxPI' or globname == 'VmaxPI':
            err,TIME,glob,globerr=get.get_PI_data(shot,globname)
            print(err,TIME,glob)
            
        if err=='ok':
            if globname == 'TImaxTWS' or globname == 'VmaxTWS' or globname == 'TImaxPI' or globname == 'VmaxPI' or globname == 'TISX' or globname == 'TESX':
                plt.errorbar(TIME,glob,globerr,label=str(shot)+'@'+globname)
            elif globname == 'PNB':
                plt.plot(TIME1,glob1,label=str(shot)+'@RFX')
                plt.plot(TIME2,glob2,label=str(shot)+'@HNBI')                
            else:
                plt.plot(TIME,glob,label=str(shot)+'@'+globname)
        legend=plt.legend(loc='upper right',fontsize='small')
        plt.show()



window.close()


