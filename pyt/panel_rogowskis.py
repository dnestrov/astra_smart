# python3 pyt/panel_rogowskis.py
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
import rog_functions as rog
import pcs_reading_functions as pcs
namerog=['DIVPSRB','DIVPSRT','HFSPSRB','HFSPSRT','MCB','MCT','GASBFLB','GASBFLT','BVLB','BVLT','DIVB','DIVT','INIVC000','MCWIRE','DIVBWIRE','BVLWIRE','DIVTWIRE','SOLWIRE','BVUBWIRE','BVUTWIRE','PSHBWIRE','PSHTWIRE','INIVC000raw','TFWIRE']

layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
          [sg.Checkbox('',default=True, key="-st40-"),
           sg.T("ST40 shot ="), sg.Input('11419', size=(6,1),key="-SHOT-"),
           sg.T("                 "),sg.Button("PFIT inputs")],
          [sg.Checkbox('Plasma',default=False, key="-plasma-"),
           sg.Checkbox('Vacuum',default=False, key="-vacuum-"),
           sg.Checkbox('in ALL node',default=False, key="-all-")],
          [sg.T("ASTRA shot="), sg.Input('13011419', size=(8,1),key="-shot-"),
           sg.T("ASTRA run"), sg.Input('220', size=(5,1), key="-run-")],
          [sg.Checkbox('DIVPSRB',default=False, key="-1-"),
           sg.Checkbox('DIVPSRT',default=False, key="-2-")],
          [sg.Checkbox('HFSPSRB',default=True, key="-3-"),
           sg.Checkbox('HFSPSRT',default=True, key="-4-")],
          [sg.Checkbox('MCB',default=False, key="-5-"),
           sg.Checkbox('MCT',default=False, key="-6-")],
          [sg.Checkbox('GASBFLB',default=False, key="-7-"),
           sg.Checkbox('GASBFLT',default=False, key="-8-")],
          [sg.Checkbox('BVLB',default=False, key="-9-"),
           sg.Checkbox('BVLT',default=False, key="-10-")],
          [sg.Checkbox('DIVB',default=False, key="-11-"),
           sg.Checkbox('DIVT',default=False, key="-12-")],
          [sg.Checkbox('INIVC000',default=False, key="-13-"),
           sg.Checkbox('INIVC000raw',default=False, key="-23-")],
          [sg.Checkbox('MCWIRE',default=False, key="-14-"),
           sg.Checkbox('DIVBWIRE',default=False, key="-15-"),
           sg.Checkbox('DIVTWIRE',default=False, key="-16-"),
           sg.Checkbox('BVLWIRE',default=False, key="-17-")],
          [sg.Checkbox('SOLWIRE',default=False, key="-18-"),
           sg.Checkbox('BVUBWIRE',default=False, key="-19-"),
           sg.Checkbox('BVUTWIRE',default=False, key="-20-")],
          [sg.Checkbox('PSHBWIRE',default=False, key="-21-"),
           sg.Checkbox('PSHTWIRE',default=False, key="-22-"),
           sg.Checkbox('TFWIRE',default=False, key="-24-")],
          [sg.Checkbox('IPL from Rogowski',default=False, key="-IPLrog-")],
          [sg.Checkbox('IPL from Rogowski raw data',default=False, key="-IPLrograw-")],
          [sg.Checkbox('IPL from POST PFIT',default=False, key="-postpfit-")],
          [sg.Checkbox('IPL from RT PFIT',default=False, key="-rtpfit-")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

    #[sg.Checkbox('',default=True, key="--")],
    


###Setting Window
window = sg.Window('Rogowski signals', layout, size=(600,650))

###Showing the Application, also GUI functions can be placed here.
while True:
    event, values = window.read()
    shots=np.array([])
    st40shot=int(values["-SHOT-"])
    shots=np.append(shots,st40shot)
    astrashot=int(values["-shot-"])
    runnumber=int(values["-run-"])
    RUNv='RUN0'+str(runnumber)
    RUNp='RUN'+str(runnumber)
    index=np.array([])
    ALL=False
    if values["-all-"]== True : ALL=True
    if values["-1-"]== True : index=np.append(index,1)
    if values["-2-"]== True : index=np.append(index,2)
    if values["-3-"]== True : index=np.append(index,3)
    if values["-4-"]== True : index=np.append(index,4)
    if values["-5-"]== True : index=np.append(index,5)
    if values["-6-"]== True : index=np.append(index,6)
    if values["-7-"]== True : index=np.append(index,7)
    if values["-8-"]== True : index=np.append(index,8)
    if values["-9-"]== True : index=np.append(index,9)
    if values["-10-"]== True : index=np.append(index,10)
    if values["-11-"]== True : index=np.append(index,11)
    if values["-12-"]== True : index=np.append(index,12)
    if values["-13-"]== True : index=np.append(index,13)
    if values["-14-"]== True : index=np.append(index,14)
    if values["-15-"]== True : index=np.append(index,15)
    if values["-16-"]== True : index=np.append(index,17)
    if values["-17-"]== True : index=np.append(index,16)
    if values["-18-"]== True : index=np.append(index,18)
    if values["-19-"]== True : index=np.append(index,19)
    if values["-20-"]== True : index=np.append(index,20)
    if values["-21-"]== True : index=np.append(index,21)
    if values["-22-"]== True : index=np.append(index,22)
    if values["-23-"]== True : index=np.append(index,23)
    if values["-24-"]== True : index=np.append(index,24)
    if event == "PFIT inputs":
        index=np.array([])
        for i in range(0,24):
            print(i,namerog[i])
            window["-"+str(i+1)+"-"].update(False)
            ok,ii=pcs.pfit_inmap(namerog[i])
            if ok == 'ok' : 
                window["-"+str(i+1)+"-"].update(True)
                index=np.append(index,i+1)
    
    #ind1=np.extract(index<=16,index)
    ind1=index
    indastra=ind1.astype(int)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        ind=index.astype(int)
        if values["-st40-"]== True :
            rog.plot_rog_exp(ind,shots,True)
            if values["-IPLrog-"]== True : rog.plot_ipl_rog_exp(shots)
            if values["-IPLrograw-"]== True : rog.plot_ipl_rog_raw_exp(shots)
            if values["-postpfit-"]== True : rog.plot_ipl_exp_ppfit(st40shot,-0.01,0.2)  
            if values["-rtpfit-"]== True : rog.plot_ipl_exp_rtpfit(st40shot)        
        if values["-vacuum-"]== True :
            if ALL:
                print(indastra,astrashot,RUNv)
                rog.plot_rog_astra_all(indastra,astrashot,RUNv)
                if values["-IPLrog-"]== True : rog.plot_ipl_rog_astra_all(astrashot,RUNv)
            else:
                rog.plot_rog_astra(indastra,astrashot,RUNv)
                if values["-IPLrog-"]== True : rog.plot_ipl_rog_astra(astrashot,RUNv)
            if values["-IPLrog-"]== True : rog.plot_ipl_astra(astrashot,RUNv)
        if values["-plasma-"]== True :
            if ALL:
                rog.plot_rog_astra_all(indastra,astrashot,RUNp)
                if values["-IPLrog-"]== True : rog.plot_ipl_rog_astra_all(astrashot,RUNp)
            else:
                rog.plot_rog_astra(indastra,astrashot,RUNp)
                if values["-IPLrog-"]== True : rog.plot_ipl_rog_astra(astrashot,RUNp)
            if values["-IPLrog-"]== True : rog.plot_ipl_astra(astrashot,RUNp)
        legend=plt.legend(loc='upper right',fontsize='small')
        plt.show()


window.close()

