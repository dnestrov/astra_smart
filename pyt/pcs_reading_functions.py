import matplotlib.pyplot as plt
from MDSplus import *
import numpy as np
import math
import sys
conn = Connection('192.168.1.7:8000')
CALC32=['IP_PFIT_ACT','RIP_PFIT_ACT','ZIP_PFIT_ACT','IMGAP_ACT','IBGAP_ACT','ITGAP_ACT','MCBGAP_ACT','MCTGAP_ACT','RXPT_T','ZXPT_T','RXPT_B','ZXPT_B','I_SOL_REF','I_BVL_REF','I_DIV_REF','I_MC_REF','I_BVUT_REF','I_BVUB_REF','I_BVU_REF','I_PSH_REF','I_SOL_ACT','I_BVL_ACT','I_DIV_ACT','I_MC_ACT','I_BVUT_ACT','I_BVUB_ACT','SUP_STATE','CISSTOP_IND','IP_PFIT_REF','RIP_PFIT_REF','ZIP_PFIT_REF']
AO33_ref=['U_REF_SOL','U_REF_DIV','U_REF_BVL','U_REF_BVUT','U_REF_BVUB']
AO33_act=['U_REF_SOL','U_REF_DIV','U_REF_BVL','U_REF_BVUT','U_REF_BVUB']
col=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf','k']
def pcs_read_sim(shotst40,run,channel,name,count):
    conn.openTree('sim_tepcs',shotst40)
    signame0=run+'ACQ2106_32:'
    signame=signame0+'CH'+channel
    if channel<10:signame=signame0+'CH00'+channel
    if channel<100:signame=signame0+'CH0'+channel
    TIME=conn.get(signame0+'PCS_TIME')
    VAR=conn.get(signame)
    color=count-len(col)*int(count/len(col))
    plt.plot(TIME,VAR,col[color],label=name+' #'+str(shotst40))
    conn.closeTree('sim_tepcs',shotst40)
    return TIME,VAR
def pcs_readcalc(shotst40,run,channel,name,count):
    conn.openTree('sim_tepcs',shotst40)
    signame0=run+'.ACQ2106_32.CALC:'
    signame=signame0+'CH'+channel
    if channel<10:signame=signame0+'CH00'+channel
    if channel<100:signame=signame0+'CH0'+channel
    TIME=conn.get(signame0+'PCS_TIME')
    VAR=conn.get(signame)
    color=count-len(col)*int(count/len(col))
    plt.plot(TIME,VAR,col[color],label=name+' #'+str(shotst40))
    conn.closeTree('sim_tepcs',shotst40)
    return TIME,VAR
def pcs_map32exp(name):
#.ACQ2106_032.CALC:CH
#PSUI_ref
    if name == 'I_SOL_REF': channel= 43
    if name == 'I_BVL_REF': channel= 44
    if name == 'I_DIV_REF': channel= 45
    if name == 'I_MC_REF': channel= 46 
    if name == 'I_BVUT_REF': channel= 47
    if name == 'I_BVUB_REF': channel= 48
    if name == 'I_PSH_REF': channel= 53
#PSUI_act 
    if name == 'I_SOL_ACT': channel= 66
    if name == 'I_BVL_ACT': channel= 67
    if name == 'I_DIV_ACT': channel= 68
    if name == 'I_MC_ACT': channel= 69
    if name == 'I_BVUT_ACT': channel= 70
    if name == 'I_BVUB_ACT': channel= 71
    if name == 'I_PSH_ACT': channel= 76
#PFIT output
    if name == 'IP_PFIT_ACT': channel=21
    if name == 'RIP_PFIT_ACT': channel= 22
    if name == 'ZIP_PFIT_ACT': channel= 23
    if name == 'R_IP_PFIT_ACT': channel= 22
    if name == 'Z_IP_PFIT_ACT': channel= 23

#controlnames_ref
    if name == 'IP_PFIT_REF': channel= 33
    if name == 'RIP_PFIT_REF': channel= 34
    if name == 'ZIP_PFIT_REF': channel= 35
    if name == 'R_IP_PFIT_REF': channel= 34
    if name == 'Z_IP_PFIT_REF': channel= 35
#REST
    if name == 'SUP_STATE': channel= 1
    if name == 'CISSTOP_IND': channel= 32
    if name == 'IMGAP_ACT': channel= 24
    if name == 'IBGAP_ACT': channel= 25
    if name == 'ITGAP_ACT': channel= 26
    if name == 'MCBGAP_ACT': channel= 27
    if name == 'MCTGAP_ACT': channel= 28
    if name == 'RXPT_T': channel= 84
    if name == 'ZXPT_T': channel= 85
    if name == 'RXPT_B': channel= 86
    if name == 'ZXPT_B': channel= 87
    return channel
def pcs_map32calc(name):
#.ACQ2106_032.CALC:CH
#PSUI_ref
    if name == 'I_SOL_REF': channel= 43
    if name == 'I_BVL_REF': channel= 44
    if name == 'I_DIV_REF': channel= 45
    if name == 'I_MC_REF': channel= 46 
    if name == 'I_BVUT_REF': channel= 47
    if name == 'I_BVUB_REF': channel= 48
    if name == 'I_PSH_REF': channel= 53
#PSUI_act 
    if name == 'I_SOL_ACT': channel= 66
    if name == 'I_BVL_ACT': channel= 67
    if name == 'I_DIV_ACT': channel= 68
    if name == 'I_MC_ACT': channel= 69
    if name == 'I_BVUT_ACT': channel= 70
    if name == 'I_BVUB_ACT': channel= 71
    if name == 'I_PSH_ACT': channel= 76
#C_act Output from ASTRA
    if name == 'IP_ASTRA_ACT': channel=21
    if name == 'RIP_ASTRA_ACT': channel= 22
    if name == 'ZIP_ASTRA_ACT': channel= 23
    if name == 'R_IP_ASTRA_ACT': channel= 22
    if name == 'Z_IP_ASTRA_ACT': channel= 23
#PFIT output
    if name == 'IP_PFIT_ACT': channel=88
    if name == 'RIP_PFIT_ACT': channel= 89
    if name == 'ZIP_PFIT_ACT': channel= 90
    if name == 'R_IP_PFIT_ACT': channel= 89
    if name == 'Z_IP_PFIT_ACT': channel= 90
#C_ref
    if name == 'IP_ASTRA_REF': channel= 33
    if name == 'RIP_ASTRA_REF': channel= 34
    if name == 'ZIP_ASTRA_REF': channel= 35
    if name == 'R_IP_ASTRA_REF': channel= 34
    if name == 'Z_IP_ASTRA_REF': channel= 35
#REST
    if name == 'SUP_STATE': channel= 1
    if name == 'CISSTOP_IND': channel= 32
    if name == 'IMGAP_ACT': channel= 24
    if name == 'IBGAP_ACT': channel= 25
    if name == 'ITGAP_ACT': channel= 26
    if name == 'MCBGAP_ACT': channel= 27
    if name == 'MCTGAP_ACT': channel= 28
    if name == 'RXPT_T': channel= 84
    if name == 'ZXPT_T': channel= 85
    if name == 'RXPT_B': channel= 86
    if name == 'ZXPT_B': channel= 87
    return channel
def pcs_map33(name):
#.ACQ2106_033:CH 
#PSUV_ref
    if name == 'U_REF_SOL': channel= 18
    if name == 'U_REF_DIV': channel= 19 
    if name == 'U_REF_BVL': channel= 20
    if name == 'U_REF_BVUT': channel= 22
    if name == 'U_REF_BVUB': channel= 23
    
    return channel
def pcs_map33AO(name):
#.ACQ2106_033.AO:CH 
#PSUI_act 
    if name == 'I_SOL_PSU': channel= 2
    if name == 'I_DIV_PSU': channel= 3
    if name == 'I_BVL_PSU': channel= 4
    if name == 'I_BVUT_PSU': channel= 6
    if name == 'I_BVUB_PSU': channel= 7
    if name == 'I_PSH_PSU': channel= 11
    if name == 'I_MC_PSU': channel= 15
#PSUV_act
    if name == 'U_MC_PSU': channel= 10
    if name == 'U_PSH_PSU': channel= 16
    if name == 'U_SOL_PSU': channel= 18
    if name == 'U_DIV_PSU': channel= 19
    if name == 'U_BVL_PSU': channel= 20
    if name == 'U_BVUT_PSU': channel= 22
    if name == 'U_BVUB_PSU': channel= 23
    return channel

def pcs_readsensors32(shot,run,treename,chan,name,count):
    if chan == 0:return
    channel=str(chan)
    try:
        conn.openTree(treename,shot)
    except:
       print('No tree for :',treename+'#'+str(shot))
       return 0,0
    signame0=run+'.ACQ2106_032:'
    signame=signame0+'CH'+channel
    if chan<100:signame=signame0+'CH0'+channel
    if chan<10:signame=signame0+'CH00'+channel
    print(shot,signame)
    try:
        VAR=conn.get(signame)
    except:
        print(signame)
        return 0,0        
    if treename == 'tepcs': 
        TIME=conn.get('dim_of(.ACQ2106_032:CH160)').data()
    else: 
        TIME=conn.get(signame0+'PCS_TIME')
    color=count-len(col)*int(count/len(col))
    plt.plot(TIME,VAR,col[color],label=name+' #'+str(shot)+'@'+run+'CH'+channel)
    plt.suptitle('MDS+ tree:'+treename)
    conn.closeTree(treename,shot)
    return TIME,VAR

def pse_readdata(shotastra,run,treename,name):
    try:
        conn.openTree(treename,shotastra)
    except:
        print('No tree for :',treename+'#'+str(shotastra))
        return 0,0
    if name.find("R_IP") != -1:name='RC_PFIT'
    if name.find("Z_IP") != -1:name='ZC_PFIT'
    if name.find("I_") != -1:name=name[:len(name)-4]
    if name == 'IP_ASTRA_REF':name='IP_PFIT'
    if name.find("U_REF")>0:return 0,0
    print(name)
    VAR=conn.get(run+'.PSE.WAVES.CVREF.'+name+':AMPLITUDES')
    TIME=conn.get(run+'.PSE.WAVES.CVREF.'+name+':TIMES')
    return TIME,VAR
def pcs_readsensors(shotastra,run,treename,chan,name,nodename):
    """
    shotastra=11424                                                         
    treename='tepcs'                                                        
    run='' 
    nodename='.ACQ2106_033.AO:'                                                                 
    chan=22
    """
    print(shotastra,run,name,nodename,chan)
    if chan == 0:return
    if chan == -1 and name.find("REF") != -1:
        TIME,VAR=pse_readdata(shotastra,run,treename,name)
        return TIME,VAR
    if chan == -1:
        return 0,0
    channel=str(chan)
    try:
        conn.openTree(treename,shotastra)
    except:
        print('No tree for :',treename+'#'+str(shotastra))
        return 0,0
    signame0=run+nodename
    signame=signame0+'CH'+channel
    signametime=run+'.ACQ2106_032:'
    if chan<100:signame=signame0+'CH0'+channel
    if chan<10:signame=signame0+'CH00'+channel
    try:
        TIME=conn.get(signametime+'PCS_TIME')
        VAR=conn.get(signame)
        conn.closeTree(treename,shotastra)
        return TIME,VAR
    except:
        print(signame)
        conn.closeTree(treename,shotastra)
        return 0,0   
def pcs_plot(TIME,VAR,shotastra,run,treename,chan,name,count):
    channel=str(chan)
    color=count-len(col)*int(count/len(col))
    try:
        len(VAR)
    except:
        print('No data',shotastra,run,treename)
        return
    if len(VAR) == len(TIME):
        if name.find('REF') != -1 or  name.find('PCS') != -1 : 
            plt.plot(TIME[1:],VAR[1:],linestyle='--',color=col[color],label=name+' #'+str(shotastra)+'@'+run+'CH'+channel)
        else: 
            plt.plot(TIME[1:],VAR[1:],col[color],label=name+' #'+str(shotastra)+'@'+run+'CH'+channel)
    
def pcs_plotPSE(TIME,VAR,shotastra,run,treename,chan,name,count):
    channel=str(chan)
    color=count-len(col)*int(count/len(col))
    try:
        len(VAR)
    except:
        print('No data',shotastra,run,treename)
        return
    if name.find("R_IP") != -1:name='RC_PFIT'
    if name.find("Z_IP") != -1:name='ZC_PFIT'
    if name == 'IP':name='IP_PFIT'
    if len(VAR) == len(TIME):
        plt.plot(TIME[1:],VAR[1:],linestyle='--',color=col[color],label=name+' #'+str(shotastra)+'@'+run+'@PSE tree')
    

def sensors_map(name):
#.ACQ2106_032:CH
    channel=999
    print('sensors_map:'+name)
    if name == 'B_BPPROBE_118': channel=97
    if name == 'B_BPPROBE_102': channel=98
    if name == 'B_BPPROBE_119': channel=99
    if name == 'B_BPPROBE_103': channel=100
    if name == 'B_BPPROBE_120': channel=101
    if name == 'B_BPPROBE_104': channel=102
    if name == 'B_BPPROBE_121': channel=103
    if name == 'B_BPPROBE_105': channel=104
    if name == 'B_BPPROBE_122': channel=105
    if name == 'B_BPPROBE_106': channel=106
    if name == 'B_BPPROBE_123': channel=107
    if name == 'B_BPPROBE_107': channel=108
    if name == 'B_BPPROBE_124': channel=109
    if name == 'B_BPPROBE_108': channel=110
    if name == 'B_BPPROBE_125': channel=111
    if name == 'B_BPPROBE_109': channel=112
    if name == 'B_BPPROBE_126': channel=113
    if name == 'B_BPPROBE_110': channel=114
    if name == 'B_BPPROBE_127': channel=115
    if name == 'B_BPPROBE_111': channel=116
    if name == 'B_BPPROBE_128': channel=117
    if name == 'B_BPPROBE_112': channel=118
    if name == 'B_BPPROBE_129': channel=119
    if name == 'B_BPPROBE_113': channel=120
    if name == 'B_BPPROBE_130': channel=121
    if name == 'B_BPPROBE_114': channel=122
    if name == 'B_BPPROBE_131': channel=123
    if name == 'B_BPPROBE_115': channel=124
    if name == 'B_BPPROBE_132': channel=125
    if name == 'B_BPPROBE_116': channel=126
    if name == 'B_BPPROBE_133': channel=127
    if name == 'B_BPPROBE_117': channel=128
    if name == 'B_BPPROBE_318': channel=130
    if name == 'B_BPPROBE_718': channel=132
    if name == 'B_BPPROBE_134': channel=158
    if name == 'B_BPPROBE_101': channel=160
    if name == 'PSI_FLOOP_005': channel=1
    if name == 'PSI_FLOOP_007': channel=3
    if name == 'PSI_FLOOP_011': channel=5
    if name == 'PSI_FLOOP_012': channel=7
    if name == 'PSI_FLOOP_013': channel=9
    if name == 'PSI_FLOOP_014': channel=11
    if name == 'PSI_FLOOP_015': channel=13
    if name == 'PSI_FLOOP_003': channel=15
    if name == 'PSI_FLOOP_016': channel=17
    if name == 'PSI_FLOOP_017': channel=19
    if name == 'PSI_FLOOP_018': channel=21
    if name == 'PSI_FLOOP_019': channel=23
    if name == 'PSI_FLOOP_020': channel=25
    if name == 'PSI_FLOOP_024': channel=27
    if name == 'PSI_FLOOP_026': channel=29
    if name == 'PSI_FLOOP_001': channel=33
    if name == 'PSI_FLOOP_002': channel=35
    if name == 'PSI_FLOOP_004': channel=37
    if name == 'PSI_FLOOP_006': channel=39
    if name == 'PSI_FLOOP_008': channel=41
    if name == 'PSI_FLOOP_009': channel=43
    if name == 'PSI_FLOOP_010': channel=45
    if name == 'PSI_FLOOP_101': channel=47
    if name == 'PSI_FLOOP_201': channel=49
    if name == 'PSI_FLOOP_021': channel=65
    if name == 'PSI_FLOOP_022': channel=67
    if name == 'PSI_FLOOP_023': channel=69
    if name == 'PSI_FLOOP_025': channel=71
    if name == 'PSI_FLOOP_027': channel=73
    if name == 'PSI_FLOOP_029': channel=75
    if name == 'PSI_FLOOP_030': channel=77
    if name == 'PSI_FLOOP_106': channel=79
    if name == 'PSI_FLOOP_212': channel=81


    if name == 'V_FLOOP_005': channel=2
    if name == 'V_FLOOP_007': channel=4
    if name == 'V_FLOOP_011': channel=6
    if name == 'V_FLOOP_012': channel=8
    if name == 'V_FLOOP_013': channel=10
    if name == 'V_FLOOP_014': channel=12
    if name == 'V_FLOOP_015': channel=14
    if name == 'V_FLOOP_003': channel=16
    if name == 'V_FLOOP_016': channel=18
    if name == 'V_FLOOP_017': channel=20
    if name == 'V_FLOOP_018': channel=22
    if name == 'V_FLOOP_019': channel=24
    if name == 'V_FLOOP_020': channel=26
    if name == 'V_FLOOP_024': channel=28
    if name == 'V_FLOOP_026': channel=30
    if name == 'V_FLOOP_001': channel=34
    if name == 'V_FLOOP_002': channel=36
    if name == 'V_FLOOP_004': channel=38
    if name == 'V_FLOOP_006': channel=40
    if name == 'V_FLOOP_008': channel=42
    if name == 'V_FLOOP_009': channel=44
    if name == 'V_FLOOP_010': channel=46
    if name == 'V_FLOOP_101': channel=48
    if name == 'V_FLOOP_201': channel=50
    if name == 'V_FLOOP_021': channel=66
    if name == 'V_FLOOP_022': channel=68
    if name == 'V_FLOOP_023': channel=70
    if name == 'V_FLOOP_025': channel=72
    if name == 'V_FLOOP_027': channel=74
    if name == 'V_FLOOP_029': channel=76
    if name == 'V_FLOOP_030': channel=78
    if name == 'V_FLOOP_106': channel=80
    if name == 'V_FLOOP_212': channel=82


    if name == 'I_ROG_INIVCHFSTOR': channel=31
    if name == 'I_ROG_BVLT': channel=51
    if name == 'I_ROG_TFWIRE': channel=53
    if name == 'I_ROG_SOLWIRE': channel=55
    if name == 'I_ROG_BVUTWIRE': channel=57
    if name == 'I_ROG_PSHTWIRE': channel=59
    if name == 'I_ROG_DIVTWIRE': channel=61
    if name == 'I_ROG_BVLB': channel=83
    if name == 'I_ROG_BVLWIRE': channel=85
    if name == 'I_ROG_MCWIRE': channel=87
    if name == 'I_ROG_BVUBWIRE': channel=89
    if name == 'I_ROG_PSHBWIRE': channel=91
    if name == 'I_ROG_DIVBWIRE': channel=93
    if name == 'I_ROG_HFSPSRB': channel=129
    if name == 'I_ROG_INIVC000': channel=131
    if name == 'I_ROG_DIVPSRB': channel=133
    if name == 'I_ROG_DIVPSRT': channel=135
    if name == 'I_ROG_MCB': channel=137
    if name == 'I_ROG_INIVC270_SPR': channel=139
    if name == 'I_ROG_MCSUP003': channel=141
    if name == 'I_ROG_MCT_SPR': channel=142
    if name == 'I_ROG_HFSPSRT': channel=143
    if name == 'I_ROG_MCT': channel=144
    if name == 'I_ROG_GASBFLB': channel=145
    if name == 'I_ROG_MCSUP001': channel=146
    if name == 'I_ROG_INIVC270': channel=147
    if name == 'I_ROG_MCSUP001_SPR': channel=148
    if name == 'I_ROG_GASBFLT': channel=150
    if name == 'I_ROG_GASBFLT_SPR': channel=152
    if name == 'I_ROG_DIVT': channel=999
    if name == 'I_ROG_DIVB': channel=999
    
    return channel
def efit_inmap(name):
    sensors_efit=["PSI_FLOOP_001 ","PSI_FLOOP_002 ","PSI_FLOOP_004 ","PSI_FLOOP_005 ","PSI_FLOOP_006 ","PSI_FLOOP_007 ","PSI_FLOOP_008 ","PSI_FLOOP_009 ","PSI_FLOOP_010 ","PSI_FLOOP_012 ","PSI_FLOOP_013 ","PSI_FLOOP_014 ","PSI_FLOOP_015 ","PSI_FLOOP_016 ","PSI_FLOOP_017 ","PSI_FLOOP_018 ","PSI_FLOOP_019 ","PSI_FLOOP_021 ","PSI_FLOOP_022 ","PSI_FLOOP_023 ","PSI_FLOOP_024 ","PSI_FLOOP_025 ","PSI_FLOOP_026 ","PSI_FLOOP_027 ","PSI_FLOOP_029 ","PSI_FLOOP_030 ","PSI_FLOOP_102 ","PSI_FLOOP_103 ","PSI_FLOOP_104 ","PSI_FLOOP_105 ","PSI_FLOOP_201 ","PSI_FLOOP_212 ","B_BPPROBE_101 ","B_BPPROBE_102 ","B_BPPROBE_103 ","B_BPPROBE_104 ","B_BPPROBE_105 ","B_BPPROBE_106 ","B_BPPROBE_107 ","B_BPPROBE_109 ","B_BPPROBE_110 ","B_BPPROBE_111 ","B_BPPROBE_112 ","B_BPPROBE_113 ","B_BPPROBE_114 ","B_BPPROBE_115 ","B_BPPROBE_116 ","B_BPPROBE_117 ","B_BPPROBE_118 ","B_BPPROBE_119 ","B_BPPROBE_120 ","B_BPPROBE_121 ","B_BPPROBE_122 ","B_BPPROBE_123 ","B_BPPROBE_124 ","B_BPPROBE_125 ","B_BPPROBE_126 ","B_BPPROBE_127 ","B_BPPROBE_129 ","B_BPPROBE_130 ","B_BPPROBE_131 ","B_BPPROBE_132 ","B_BPPROBE_133 ","B_BPPROBE_134 ","I_ROG_INIVC000","I_ROG_DIVT ","I_ROG_DIVB ","I_ROG_BVLT ","I_ROG_BVLB ","I_ROG_MCT ","I_ROG_MCB ","I_ROG_GASBFLT ","I_ROG_GASBFLB "]

# from CV_PFIT_sensor_index =
def pfit_inmap(name):
    chann=[   160,    98,   102,   104,   112,   118,   120,   122,   124,   126,    97,    99,   101,   103,   105,   109,   111,   113,   115,   117,   121,   123,   125,   158,    33,    35,    37,     1,    39,     3,    41,    43,    45,     5,     7,     9,    11,    13,    17,    19,    21,    23,    25,    65,    69,    27,    71,    29,    73,    75,    49,    81,   131,    51,    83,   145,     6,    26,     8,    24]
    sensors_rtpfit=['B_BPPROBE_101', 'B_BPPROBE_102', 'B_BPPROBE_104', 'B_BPPROBE_105',
             'B_BPPROBE_109', 'B_BPPROBE_112', 'B_BPPROBE_113', 'B_BPPROBE_114',
             'B_BPPROBE_115', 'B_BPPROBE_116', 'B_BPPROBE_118', 'B_BPPROBE_119',
             'B_BPPROBE_120', 'B_BPPROBE_121', 'B_BPPROBE_122', 'B_BPPROBE_124',
             'B_BPPROBE_125', 'B_BPPROBE_126', 'B_BPPROBE_127', 'B_BPPROBE_128',
             'B_BPPROBE_130', 'B_BPPROBE_131', 'B_BPPROBE_132', 'B_BPPROBE_134',
             'PSI_FLOOP_001', 'PSI_FLOOP_002', 'PSI_FLOOP_004', 'PSI_FLOOP_005',
             'PSI_FLOOP_006', 'PSI_FLOOP_007', 'PSI_FLOOP_008', 'PSI_FLOOP_009',
             'PSI_FLOOP_010', 'PSI_FLOOP_011', 'PSI_FLOOP_012', 'PSI_FLOOP_013',
             'PSI_FLOOP_014', 'PSI_FLOOP_015', 'PSI_FLOOP_016', 'PSI_FLOOP_017',
             'PSI_FLOOP_018', 'PSI_FLOOP_019', 'PSI_FLOOP_020', 'PSI_FLOOP_021',
             'PSI_FLOOP_023', 'PSI_FLOOP_024', 'PSI_FLOOP_025', 'PSI_FLOOP_026',
             'PSI_FLOOP_027', 'PSI_FLOOP_029', 'PSI_FLOOP_201', 'PSI_FLOOP_212',
             'I_ROG_INIVC000', 'I_ROG_BVLT', 'I_ROG_BVLB', 'I_ROG_GASBFLB',
             'V_FLOOP_011', 'V_FLOOP_020', 'V_FLOOP_012', 'V_FLOOP_019',
             "REG_I_ROG_IVC ","REG_I_ROG_OVC ","REG_I_ROG_GASBFLT"]

    sensors_postpfit=["B_BPPROBE_101 ","B_BPPROBE_102 ","B_BPPROBE_104 ","B_BPPROBE_105 ","B_BPPROBE_109 ","B_BPPROBE_112 ","B_BPPROBE_113 ","B_BPPROBE_114 ","B_BPPROBE_115 ","B_BPPROBE_116 ","B_BPPROBE_118 ","B_BPPROBE_119 ","B_BPPROBE_120 ","B_BPPROBE_121 ","B_BPPROBE_122 ","B_BPPROBE_124 ","B_BPPROBE_125 ","B_BPPROBE_126 ","B_BPPROBE_127 ","B_BPPROBE_128 ","B_BPPROBE_130 ","B_BPPROBE_131 ","B_BPPROBE_132 ","B_BPPROBE_134 ","PSI_FLOOP_001 ","PSI_FLOOP_002 ","PSI_FLOOP_004 ","PSI_FLOOP_005 ","PSI_FLOOP_006 ","PSI_FLOOP_007 ","PSI_FLOOP_008 ","PSI_FLOOP_009 ","PSI_FLOOP_010 ","PSI_FLOOP_011 ","PSI_FLOOP_012 ","PSI_FLOOP_013 ","PSI_FLOOP_014 ","PSI_FLOOP_015 ","PSI_FLOOP_016 ","PSI_FLOOP_017 ","PSI_FLOOP_018 ","PSI_FLOOP_019 ","PSI_FLOOP_020 ","PSI_FLOOP_021 ","PSI_FLOOP_023 ","PSI_FLOOP_024 ","PSI_FLOOP_025 ","PSI_FLOOP_026 ","PSI_FLOOP_027 ","PSI_FLOOP_029 ","PSI_FLOOP_101 ","PSI_FLOOP_102 ","PSI_FLOOP_103 ","PSI_FLOOP_104 ","PSI_FLOOP_105 ","PSI_FLOOP_106 ","PSI_FLOOP_201 ","PSI_FLOOP_212 ","I_ROG_INIVC000 ","I_ROG_BVLT ","I_ROG_BVLB ","I_ROG_GASBFLB ","I_ROG_DIVT ","I_ROG_DIVB ","I_ROG_HFSPSRB ","I_ROG_DIVPSRT ","REG_I_ROG_IVC ","REG_I_ROG_OVC ","REG_I_ROG_ERINGT ","REG_I_ROG_ERINGB ","REG_I_ROG_DIVPSRB","REG_I_ROG_HFSPSRT","REG_I_ROG_GASBFLT"]
    ok='--'
    sensors=sensors_rtpfit
    for i in range(0,len(sensors)):
        name0 = 'I_ROG_'+name
        if name[:7] == 'BPPROBE':name0='B_'+name
        if name[:5] =='FLOOP':name0='PSI_'+name
        print(sensors[i],name,name0)
        if sensors[i] == name0:
            ok='ok'
            #print(i,chann[i])
            return ok,chann[i] 
    return ok,999
        
    """
    file='../pcs/config/PCS_IO.csv'
    file1=open(file,'r')
    Lines = file1.readlines()
    sensors=np.array([])
    for j in range(0,len(chann)):
        print(chann[j])
        for i in range (0,len(Lines)):
            line=Lines[i]
            AI=line.split(',')[0]
            name=line.split(',')[1]
            if AI[0:2] == 'AI' : 
                if int(AI[3:6]) == chann[j]: 
                    print(name)
                    sensors=np.append(sensors,name)
    return sensors
    
    for i in range (0,len(Lines)):
        line=Lines[i]
        AI=line.split(',')[0]
        name=line.split(',')[1]
        if AI[0:2] == 'AI' :
            #if name[0:9] == 'B_BPPROBE':
            #if name[0:9] == 'PSI_FLOOP':
            if name[0:5] == 'I_ROG':
                print('    if name == \''+name+'\': channel='+ str(int(AI[3:6])))

    """
def pfit_calibration(shotst40):
    conn.openTree('pfit',shotst40)
    names='RT_RUN08.PRESHOT.PFITA.MATRICES:SENSOR_NAMES'
    wei='RT_RUN08.PRESHOT.PFITA.MATRICES:WEIGHTS'
    namep='RT_RUN08.PRESHOT.PFITA.MATRICES:PSU_NAMES'
    n=conn.get(names)
    psu=conn.get(namep)
    w=conn.get(wei)
    for i in range(0,len(n)): print(n[i],w[i,i])
    return n,wei
