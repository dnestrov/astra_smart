#python3 pyt/mkrun_smlnk.py
from MDSplus import *
from numpy import *
import mdsHelpers as mh
from importlib import reload
reload(mh)
import vac_astra_tree as vacuu
import st40_astra_tree as astra
#astra.create(13009086,'RUN4','RUN2 lower density P2.2 magnetic configuration')
#vac.create(13010820,'RUN04','RUN01 with current filament at R=0.8m')
#vacuu.create(13011560,'RUN01','run in FENIX')
#astra.create(13011560,'RUN1','run in FENIX')
#vacuu.create(13011560,'RUN0120','run in FENIX')
#astra.create(13011560,'RUN120','run in FENIX')
#vacuu.modifyhelp(13011560,'RUN0120','run in FENIX w/o NUBEAM')
#astra.modifyhelp(13011560,'RUN120','run in FENIX w/o NUBEAM')
#vacuu.create(13011560,'RUN05','test')
#astra.create(13011560,'RUN5','test')
astra.modifyhelp(13001092,'RUN104','FBE starts with EFIT geom on 10ms')
astra.modifyhelp(13001092,'RUN105','IPL starts from -1.75ms')

