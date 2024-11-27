# python3 pyt/call_make_exp.py 11048 no
# python3 pyt/call_make_exp.py 11048 no
import sys
import make_exp as m
shotnumber=int(sys.argv[1])
tofile=False
print(len(sys.argv))
if len(sys.argv) > 2 :
    save=str(sys.argv[2])
    if save.upper() == 'YES':tofile=True
print('shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filter,ifHDA,runHDA,ifBDA,bdarange,tofile')

m.printout(shotnumber,0.01, 0.15, 0.03, 0.04, 'P2.3', 1, 'BEST', 0, 0, 64, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0.001, 0,' ', 1, 0.0,tofile)

#m.printout(shotnumber,0.01, 0.15, 0.03, 0.04, 'P2.3', 1, 'BEST', 0, 0, 64, 0, 0, 1, 2, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0.001, 0,' ', 0, tofile)

#m.printout(shotnumber,11100 0.01 0.15 0.03 0.05 P2.3 1 BEST 0 0 64 0 0 0 2 1 0 0 0 0 0 1 0 0 0 0.001 0  1 0.0 , tofile)
#m.printout(shotnumber,time1,time2,t1,t2,Program_configuration,efit,efitnumber,pfit,ifBND,ntheta,ifPSU,ifNIR,ifSMM,ifNBI,ifXRCS,ifAr,ifSym,ifTWSTi,ifTWSVtor,ifPITi,ifPIVtor,ifTS,ifTSHFS,ifTSLFS,filt,ifHDA,runHDA,ifBDA,tofile)


