# python3 pyt/panel_calcexp_refvsact.py
import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
import pcs_reading_functions as pcs
import read_astra_globals as astra
try:
    import PySimpleGUI as sg    # Some user's python environment has PySimpleGUI (no longer free)
except:
    import FreeSimpleGUI as sg  # Other user's pythong environment has FreeSimpleGUI,
    sg.set_options(scaling=1.4) # e.g. "transp_gui311_env" conda env
FONTSIZE=12
shotastra=13011419
RUN='RUN220'
conn = Connection('192.168.1.7:8000')
r=Tree('astra',13011228).getNode("\\TOP").getChildren().getPath().data() 
g=Tree('astra',13011228).getNode("\\TOP.RUN613.GLOBAL").getNodeWild('*').getPath().data()
run=np.array([])
win=0
winx=0
channel=0
for i in range(0,len(r)):
    el=r[i][12:20].decode().strip()
    #print(el) 
    run = np.append(run,el)

runs=run.tolist()

combo_style={'size':(10,1)}
PSUI_ref=['I_SOL_REF','I_BVL_REF','I_DIV_REF','I_BVUT_REF','I_BVUB_REF','I_PSH_REF','I_MC_REF']
PSUI_act=['I_SOL_ACT','I_BVL_ACT','I_DIV_ACT','I_BVUT_ACT','I_BVUB_ACT','I_PSH_ACT','I_MC_ACT']
C_act=['IP_PFIT_ACT','RIP_PFIT_ACT','ZIP_PFIT_ACT']
C_ref=['IP_PFIT_REF','RIP_PFIT_REF','ZIP_PFIT_REF']
REST=['SUP_STATE','CISSTOP_IND','IMGAP_ACT','IBGAP_ACT','ITGAP_ACT','MCBGAP_ACT','MCTGAP_ACT','RXPT_T','ZXPT_T','RXPT_B','ZXPT_B']
PSUV_ref=['U_REF_SOL','U_REF_BVL','U_REF_DIV','U_REF_BVUT','U_REF_BVUB','U_REF_PSH']
PSUV_act=['U_SOL_PSU','U_BVL_PSU','U_DIV_PSU','U_BVUT_PSU','U_BVUB_PSU','U_PSH_PSU','U_MC_PSU']
coilnames=['SOL','BVL','DIV','BVUT','BVUB','PSH','MC']
controlnames=['IP','RIP','R_IP','ZIP','Z_IP']
pfitcontrolnames=['IP','RIP','R_IP','ZIP','Z_IP']

count=0
col_ref=30
col_refx=31
combobox1=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1-')
combobox2=sg.InputCombo(values=coilnames, **combo_style, enable_events=True, key='-COMBO2-')
combobox3=sg.InputCombo(values=coilnames[:5], **combo_style, enable_events=True, key='-COMBO3-')
combobox4=sg.InputCombo(values=controlnames, **combo_style, enable_events=True, key='-COMBO4-')
combobox41=sg.InputCombo(values=pfitcontrolnames, **combo_style, enable_events=True, key='-COMBO41-')
combobox5=sg.InputCombo(values=REST, **combo_style, enable_events=True, key='-COMBO5-')

combobox1x=sg.InputCombo(values=['',], **combo_style, enable_events=True, key='-COMBO1x-')
combobox2x=sg.InputCombo(values=coilnames, **combo_style, enable_events=True, key='-COMBO2x-')
combobox3x=sg.InputCombo(values=coilnames[:5], **combo_style, enable_events=True, key='-COMBO3x-')
combobox4x=sg.InputCombo(values=controlnames, **combo_style, enable_events=True, key='-COMBO4x-')
combobox5x=sg.InputCombo(values=REST, **combo_style, enable_events=True, key='-COMBO5x-')

plt.figure(figsize=(10, 3))
plt.rc('font', size=FONTSIZE)
layout = [[sg.T("")],
          [sg.T("        "), sg.Button('make plot',size=(20,4)),
           sg.T("        "), sg.Button('Exit',size=(4,2))], 
          [sg.Radio('Reference data from channels', "RADIO1", default=False, key="-channels-"),
           sg.Radio('Reference data from PSE', "RADIO1", default=True, key="-PSE-")],
          [sg.Checkbox('ASTRA',default=True, key="-ASTRA-"),
           sg.T("ASTRA shot="), sg.Input('13012515', size=(8,1),key="-shotastra-"),
           sg.Button('reread shot',size=(10,1)),
           sg.T("RUN"),combobox1],
          [sg.T("currents"),combobox2,
           sg.T("voltages"),combobox3],
          [sg.T("controlled"),
           #sg.Radio('sim_tepcs', "RADIO1", default=True, key="-sim_tepcs-"),
           #sg.Radio('sophia', "RADIO1", default=False, key="-sophia-"),
           sg.Checkbox('ASTRA tree',default=False, key="-astraglob-"),combobox4],
          [sg.T("other"),combobox5],
          [sg.T("PFIT output"),combobox41],
          [sg.Checkbox('ST40',default=False, key="-exp-"),
           sg.T("ST40 shot ="), sg.Input('11419', size=(6,1),key="-SHOT-")],
          [sg.T("currents"),combobox2x],
          [sg.T("voltages"),combobox3x,
           sg.Checkbox('prescribed',default=True, key="-prescribed-"),
           sg.Checkbox('measured',default=False, key="-measured-")],
          [sg.T("controlled"),combobox4x,
           sg.T("other"),combobox5x],
          [sg.Checkbox('new figure',default=False, key="-newfig-")],
          [sg.T("")],[sg.T("")]]


window = sg.Window('REF vs ACT - ASTRA vs EXP ', layout, size=(900, 500))
count=0

while True:
    event, values = window.read()
    shotastra=int(values["-shotastra-"])
    shotst40=int(values["-SHOT-"])
    #treename='sim_tepcs' 
    title=''
    if event == "reread shot":
        r=Tree('astra',shotastra).getNode("\\TOP").getChildren().getPath().data()    
        run=np.array([])
        for i in range(0,len(r)):
            el=r[i][12:20].decode().strip()
            print(el) 
            try:
                if el[3]  !='0':run = np.append(run,el)
            except:pass
        runs=run.tolist()
        combobox1.Update(values=runs)
    if event == '-COMBO1-' :
        RUN= values['-COMBO1-']
#        print(RUN+':HELP')
        conn.openTree('astra',shotastra)
        text=conn.get(RUN+':HELP')
        print('Comment for '+RUN+':')
        print(text)
    if event == '-COMBO2-' :
        coilname= values['-COMBO2-']
        channel_ref=pcs.pcs_map32calc('I_'+coilname+'_REF')
        channel_act=pcs.pcs_map32calc('I_'+coilname+'_ACT')
        win=2
    if event == '-COMBO3-' :
        coilname= values['-COMBO3-']
        channel_ref=pcs.pcs_map33('U_REF_'+coilname)
        channel_act=pcs.pcs_map33AO('U_'+coilname+'_PSU')
        win=3
    if event == '-COMBO4-' :
        cname= values['-COMBO4-']
        channel_ref=pcs.pcs_map32calc(cname+'_ASTRA_REF')
        channel_act=pcs.pcs_map32calc(cname+'_ASTRA_ACT')
        if cname=='R_IP' or cname=='Z_IP':
            channel_ip_ref=pcs.pcs_map32calc('IP_ASTRA_REF')
            channel_ip_act=pcs.pcs_map32calc('IP_ASTRA_ACT')            
        win=4
    if event == '-COMBO41-' :
        cname= values['-COMBO41-']
        channel_act=pcs.pcs_map32calc(cname+'_PFIT_ACT')
        if cname=='R_IP' or cname=='Z_IP':
            channel_ip_act=pcs.pcs_map32calc('IP_PFIT_ACT')            
        win=41
    if event == '-COMBO5-' :
        othername= values['-COMBO5-']
        channel=pcs.pcs_map32calc(othername)
        win=5
    if event == '-COMBO2x-' :
        coilname= values['-COMBO2x-']
        channel_refx=pcs.pcs_map32exp('I_'+coilname+'_REF')
        channel_actx=pcs.pcs_map32exp('I_'+coilname+'_ACT')
        winx=2
    if event == '-COMBO3x-' :
        coilname= values['-COMBO3x-']
        channel_refx=pcs.pcs_map33('U_REF_'+coilname)
        channel_actx=pcs.pcs_map33AO('U_'+coilname+'_PSU')
        winx=3
    if event == '-COMBO4x-' :
        cname= values['-COMBO4x-']
        channel_refx=pcs.pcs_map32exp(cname+'_PFIT_REF')
        channel_actx=pcs.pcs_map32exp(cname+'_PFIT_ACT')
        if cname=='R_IP' or cname=='Z_IP':
            channel_ip_refx=pcs.pcs_map32exp('IP_PFIT_REF')
            channel_ip_actx=pcs.pcs_map32exp('IP_PFIT_ACT')            
        winx=4
    if event == '-COMBO5x-' :
        othername= values['-COMBO5x-']
        channelx=pcs.pcs_map32exp(othername)
        winx=5
    if values['-PSE-']:
        channel_ref=-1
        channel_ip_ref=-1
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event== "make plot":
        if values["-newfig-"] == True : 
            plt.figure(figsize=(10, 3))
            plt.rc('font', size=FONTSIZE)
            count=0
        if values["-ASTRA-"] == True :
            try:
                conn.openTree('sim_tepcs',shotastra)
                signame0=RUN+'.ACQ2106_032:'
                TIME=conn.get(signame0+'PCS_TIME')
                treename='sim_tepcs'
            except:
                print('No sim_tepcs tree for shot #',shotastra,RUN)
                print('Try SOPHIA tree')
                treename='SOPHIA'
            title=title+treename+' '
            print(treename+' win=',win)
            if win == 2 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,'I_'+coilname+'_ACT',nodename)
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'I_'+coilname+'_ACT',count)
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,'I_'+coilname+'_REF',nodename)
                if values['-PSE-']:
                    pcs.pcs_plotPSE(TIME,VAR,shotastra,RUN,treename,channel_ref,'I_'+coilname+'_REF',col_ref-1)
                else:
                    pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_ref,'I_'+coilname+'_REF',col_ref)
            if win == 3 :
                nodename='.ACQ2106_033.AO:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,'U_'+coilname+'_PSU',nodename)
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'U_'+coilname+'_PSU',count)
                nodename='.ACQ2106_033:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,'U_REF_'+coilname,nodename)
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,'U_REF_'+coilname,col_ref)
            if win == 4 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',nodename)
                if cname=='R_IP' or cname=='Z_IP':
                    TIME,VAR2=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ip_act,'IP_ASTRA_ACT',nodename)
                    pcs.pcs_plot(TIME,VAR/VAR2,shotastra,RUN,treename,channel_act,cname+'_ASTRA_ACT',count)
                else:
                    pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_act,cname+'_ASTRA_ACT',count)
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ref,cname+'_ASTRA_REF',nodename)
                if values['-PSE-']:
                    pcs.pcs_plotPSE(TIME,VAR,shotastra,RUN,treename,channel_ref,cname,col_ref-1)
                else:
                    if cname=='R_IP' or cname=='Z_IP'  :
                        TIME,VAR2=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ip_ref,'IP_ASTRA_REF',nodename)
                        pcs.pcs_plot(TIME,VAR/VAR2,shotastra,RUN,treename,channel_ref,cname+'_ASTRA_REF',col_ref)
                    else:
                        pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel_ref,cname,col_ref)
                if values['-astraglob-']:
                    TIME,VAR=astra.calc_global(shotastra,cname,RUN)
            if win == 41 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',nodename)
                ind=np.where(TIME>0)
                if cname=='R_IP' or cname=='Z_IP':
                    TIME,VAR2=pcs.pcs_readsensors(shotastra,RUN,treename,channel_ip_act,'IP_PFIT_ACT',nodename)
                    VAR1=VAR/VAR2
                else:
                    VAR1=VAR
                pcs.pcs_plot(TIME[ind],VAR[ind],shotastra,RUN,treename,channel_act,cname+'_PFIT_ACT',count)
            if win == 5 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotastra,RUN,treename,channel,othername,nodename)
                pcs.pcs_plot(TIME,VAR,shotastra,RUN,treename,channel,othername,count)
            count+=1
        if values["-exp-"] == True :
            treename='tepcs' 
            title=title+treename+' '
            RUNx=''
            print('tepcs tree, winx=',winx)
            if winx == 2 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_actx,'I_'+coilname+'_ACT',nodename)
                pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channel_actx,'I_'+coilname+'_ACT',count)
                TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_refx,'I_'+coilname+'_REF',nodename)
                pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channel_actx,'I_'+coilname+'_REF',col_refx)
            if winx == 3 :
                if values["-prescribed-"] == True : 
                    nodename='.ACQ2106_033.AO:'
                    TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_actx,'U_PCS_'+coilname,nodename)
                    pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channel_actx,'U_PCS_'+coilname,count)
                if values["-measured-"] == True :
                    nodename='.ACQ2106_033:'
                    TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_refx,'U_PSU_'+coilname,nodename)
                    count+=1
                    VAR68=VAR[::5]
                    pcs.pcs_plot(TIME,VAR68,shotst40,RUNx,treename,channel_actx,'U_PSU_'+coilname,count)
            if winx == 4 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_actx,cname+'_PFIT_ACT',nodename)
                if cname=='R_IP' or cname=='Z_IP':
                    TIME,VAR2=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_ip_actx,'IP_PFIT_ACT',nodename)
                    pcs.pcs_plot(TIME,VAR/VAR2,shotst40,RUNx,treename,channel_actx,cname+'_PFIT_ACT',count)
                else:
                    pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channel_actx,cname+'_PFIT_ACT',count)
                TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_refx,cname+'_PFIT_REF',nodename)
                if cname=='R_IP' or cname=='Z_IP':
                    TIME,VAR2=pcs.pcs_readsensors(shotst40,RUNx,treename,channel_ip_refx,'IP_PFIT_REF',nodename)
                    pcs.pcs_plot(TIME,VAR/VAR2,shotst40,RUNx,treename,channel_refx,cname+'_PFIT_REF',count)
                else:
                    pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channel_refx,cname+'_PFIT_REF',count)
            if winx == 5 :
                nodename='.ACQ2106_032.CALC:'
                TIME,VAR=pcs.pcs_readsensors(shotst40,RUNx,treename,channelx,othername,nodename)
                pcs.pcs_plot(TIME,VAR,shotst40,RUNx,treename,channelx,othername,count)

            count+=1
        plt.suptitle(title)
        legend=plt.legend(loc='upper left',fontsize='small')
        plt.show()


window.close()


