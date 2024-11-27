# python3 pyt/panel_exp_refvsact.py
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
import pcs_reading_functions as pcs
conn = Connection('192.168.1.7:8000')
"""
r=Tree('astra',13011228).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',13011228).getNode("\\TOP.RUN613.GLOBAL").getNodeWild('*').getPath().data()
run=np.array([])
win=0
channel=0
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    #print(el) 
    run = np.append(run,el)

runs=run.tolist()
"""
combo_style={'size':(20,1)}
PSUI_ref=['I_SOL_REF','I_BVL_REF','I_DIV_REF','I_BVUT_REF','I_BVUB_REF','I_PSH_REF','I_MC_REF']
PSUI_act=['I_SOL_ACT','I_BVL_ACT','I_DIV_ACT','I_BVUT_ACT','I_BVUB_ACT','I_PSH_ACT','I_MC_ACT']
C_act=['IP_PFIT_ACT','RIP_PFIT_ACT','ZIP_PFIT_ACT']
C_ref=['IP_PFIT_REF','RIP_PFIT_REF','ZIP_PFIT_REF']
REST=['SUP_STATE','CISSTOP_IND','IMGAP_ACT','IBGAP_ACT','ITGAP_ACT','MCBGAP_ACT','MCTGAP_ACT','RXPT_T','ZXPT_T','RXPT_B','ZXPT_B']
PSUV_ref=['U_REF_SOL','U_REF_BVL','U_REF_DIV','U_REF_BVUT','U_REF_BVUB','U_REF_PSH']
PSUV_act=['U_SOL_PSU','U_BVL_PSU','U_DIV_PSU','U_BVUT_PSU','U_BVUB_PSU','U_PSH_PSU','U_MC_PSU']
coilnames=['SOL','BVL','DIV','BVUT','BVUB','PSH','MC']
controlnames=['IP','RIP','R_IP','ZIP','Z_IP']

count=0
col_ref=30
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=coilnames, **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=coilnames[:5], **combo_style, enable_events=True, key='-COMBO3-')
combobox4=sg.InputCombo(values=controlnames, **combo_style, enable_events=True, key='-COMBO4-')
combobox5=sg.InputCombo(values=REST, **combo_style, enable_events=True, key='-COMBO5-')

layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4))], [sg.T("")],
          [sg.T("ST40 shot="), sg.Input('11560', size=(8,1),key="-shot-")],
          [sg.T("currents"),combobox2],
          [sg.T("voltages"),combobox3,
           sg.Checkbox('prescribed',default=True, key="-prescribed-"),
           sg.Checkbox('measured',default=False, key="-measured-")],
          [sg.T("controlled"),combobox4],
          [sg.T("other"),combobox5],
          [sg.T("")],[sg.T("")],
          [sg.T("        "), sg.Button('Exit',size=(4,2))], [sg.T("")]]

window = sg.Window('REF vs ACT in tepcs ', layout, size=(715, 500))
count=0
treename='tepcs'
RUN=''
while True:
    event, values = window.read()
    shotastra=int(values["-shot-"])
    """    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el) 
            if el[3]  !='0':run = np.append(run,el)
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
    """
    if event == '-COMBO2-' :
        coilname= values['-COMBO2-']
        channel_ref=pcs.pcs_map32exp('I_'+coilname+'_REF')
        channel_act=pcs.pcs_map32exp('I_'+coilname+'_ACT')
        win=2
    if event == '-COMBO3-' :
        coilname= values['-COMBO3-']
        channel_ref=pcs.pcs_map33('U_REF_'+coilname)
        channel_act=pcs.pcs_map33AO('U_'+coilname+'_PSU')
        win=3
    if event == '-COMBO4-' :
        cname= values['-COMBO4-']
        channel_ref=pcs.pcs_map32exp(cname+'_PFIT_REF')
        channel_act=pcs.pcs_map32exp(cname+'_PFIT_ACT')
        if cname=='R_IP' or cname=='Z_IP':
            channel_ip_ref=pcs.pcs_map32exp('IP_PFIT_REF')
            channel_ip_act=pcs.pcs_map32exp('IP_PFIT_ACT')            
        win=4
    if event == '-COMBO5-' :
        othername= values['-COMBO5-']
        channel=pcs.pcs_map32exp(othername)
        win=5
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        if win == 2 :
            nodename='.ACQ2106_032.CALC:'
            TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,'I_'+coilname+'_ACT',nodename)
            pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'I_'+coilname+'_ACT',count)
            TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,'I_'+coilname+'_REF',nodename)
            pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'I_'+coilname+'_REF',col_ref)
        if win == 3 :
            if values["-prescribed-"] == True : 
                nodename='.ACQ2106_033.AO:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,'U_'+coilname,nodename)
                print('U_'+coilname+'_PSU',len(TIME),len(VAR))
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'U_'+coilname,count)
            if values["-measured-"] == True :
                nodename='.ACQ2106_033:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,'U_PSU_'+coilname,nodename)
                print('U_REF_'+coilname,len(TIME),len(VAR))
                count+=1
                VAR68=VAR[::5]
                pcs.pcs_plot(TIME,VAR68,shotastra,RUN,treename,channel_act,'U_PSU_'+coilname,count)
        if win == 4 :
            nodename='.ACQ2106_032.CALC:'
            TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',nodename)
            if cname=='R_IP' or cname=='Z_IP':
                TIME,VAR2=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ip_act,'IP_PFIT_ACT',nodename)
                pcs.pcs_plot(TIME,VAR/VAR2,shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',count)
            else:
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',count)
            TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,cname+'_PFIT_REF',nodename)
            if cname=='R_IP' or cname=='Z_IP':
                TIME,VAR2=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ip_ref,'IP_PFIT_REF',nodename)
                pcs.pcs_plot(TIME,VAR/VAR2,shotastra,RUN,treename,channel_ref,cname+'_PFIT_REF',col_ref)
            else:
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_ref,cname+'_PFIT_REF',col_ref)
        if win == 5 :
            nodename='.ACQ2106_032.CALC:'
            TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel,othername,nodename)
            pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel,othername,count)
        count+=1
        plt.suptitle(treename)
        legend=plt.legend(loc='upper left',fontsize='small') 
        plt.show()


window.close()


