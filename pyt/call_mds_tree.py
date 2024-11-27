#python3 pyt/call_mds_tree.py $shot $runASTRA $range  $text1 $text2 $text3
#python3 pyt/call_mds_tree.py 11048 1 13000000 help line
import sys
import st40_astra_tree as astra
shotnumber=int(sys.argv[1])
run=int(sys.argv[2])
rang=int(sys.argv[3])
text=''
for j in range(4,len(sys.argv)):
    text=text+' '+str(sys.argv[j])

RUN='RUN'+str(run)
ok=astra.create(rang+shotnumber,RUN,text)
if ok:print('Plasma tree created',rang+shotnumber,RUN,text)
if not ok:print('done nothing')
