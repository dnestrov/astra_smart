#python3 mkshot.py ??000000 9120 RUN500 test with strahl
from MDSplus import *
from numpy import *
import mdsHelpers as mh
from imp import reload
reload(mh)
import sys
import st40_astra_tree as a
ran=int(sys.argv[1])
shotnumber=int(sys.argv[2])
runnumber=str(sys.argv[3])
text=''
for j in range(4,len(sys.argv)):
    text=text+' '+str(sys.argv[j])
print(ran+shotnumber,runnumber,text)
a.create(ran+shotnumber,runnumber,text)
