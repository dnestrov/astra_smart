import numpy as np
import matplotlib.pyplot as plt
import matplotlib
WK='EFIT'
def plot_psi(WK,text,inverse,title):
    matplotlib.use('TkAgg')
# Clear figure and console


    # Open file for reading and writing
    fid=open(WK+'/out.wr', 'r+')
    a1 = fid.readline().strip()
    a2 = fid.readline().strip()
    ni = int(a1.split()[0])
    nj = int(a1.split()[1])
    ni1 = int(a1.split()[2])
    nj1 = int(a1.split()[3])
    ni2 = int(a1.split()[4])
    nj2 = int(a1.split()[5])
    nxb = int(a2)

    r=[float(x) for x in next(fid).split()]
    while len(r) < ni :
        r=np.append(r,[float(x) for x in next(fid).split()])

    z=[float(x) for x in next(fid).split()]
    while len(z) < nj:
        z=np.append(z,[float(x) for x in next(fid).split()])

    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    psi=y.reshape((nj, ni))

    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    cur=y.reshape((nj, ni))
    
    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    ipr=y.reshape((nj, ni))

    rm,zm,psim=[float(x) for x in next(fid).split()]
    rx,zx,psix=[float(x) for x in next(fid).split()]
    psib=float(next(fid))

    rxb=[float(x) for x in next(fid).split()]
    while len(rxb) < nxb:
        rxb=np.append(rxb,[float(x) for x in next(fid).split()])

    zxb=[float(x) for x in next(fid).split()]
    while len(zxb) < nxb:
        zxb=np.append(zxb,[float(x) for x in next(fid).split()])

    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    psii=y.reshape((nj, ni))

    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    psie=y.reshape((nj, ni))

    y=[float(x) for x in next(fid).split()]
    while len(y) < ni*nj:
        y=np.append(y,[float(x) for x in next(fid).split()])
    psin=y.reshape((nj, ni))

    fid.close()
    # Open another file for reading and writing
    with open(WK+'/ecur.wr', 'r+') as fid:
        a1 = fid.readline().strip()
        nk = int(a1.split()[0])
        nkk = int(a1.split()[1])
        rk=[float(x) for x in next(fid).split()]
        while len(rk) < nk :
            rk=np.append(rk,[float(x) for x in next(fid).split()])
        zk=[float(x) for x in next(fid).split()]
        while len(zk) < nk :
            zk=np.append(zk,[float(x) for x in next(fid).split()])

    # Open another file for reading
    with open(WK+'/astrafit.wr', 'r') as fid:
        nbn = int(fid.readline().strip())
        rbn = np.zeros(nbn)
        zbn = np.zeros(nbn)
        for i in range(nbn):
            rzbn = np.array([float(x) for x in fid.readline().strip().split()])
            rbn[i] = rzbn[0]
            zbn[i] = rzbn[1]

        try:
            ncp = int(fid.readline().strip())
            rcp = np.zeros(ncp)
            zcp = np.zeros(ncp)
            for i in range(ncp):
                rzcp = np.array([float(x) for x in fid.readline().strip().split()])
                rcp[i] = rzcp[0]
                zcp[i] = rzcp[1]
        except:ncp=0

        # Open another file for reading and writing
    with open(WK+'/limpnt.dat', 'r+') as fid:
        nl = int(fid.readline().strip())
        rl = np.zeros(nl)
        zl = np.zeros(nl)
        for il in range(nl):
            arrd = np.array([float(x) for x in fid.readline().strip().split()])
            rl[il] = arrd[0]
            zl[il] = arrd[1]

    # Plotting
    plt.figure(figsize=(4, 6))
    plt.clf()
    plt.axis('equal')
    #plt.gca().set_box_aspect(1)
    plt.jet
    plt.contour(r, z, psi, 50)
    plt.plot(rm, zm, 'b+')
    plt.plot(rk, zk, 'k+')
    plt.plot(rbn, zbn, 'r.')
    plt.plot(rxb, zxb, 'b.')
    plt.plot(rx, zx, 'bx')
    plt.plot(rl, zl, 'k.')
    if inverse:
        plt.suptitle('SpiderInverse in '+WK)
        plt.title(title)
    else:
        plt.suptitle('SpiderDirect in '+WK)
        plt.title(title)
    if ncp>0:plt.plot(rcp, zcp, 'g*')
    if text:coil_spidercurtext(WK,inverse)
    plt.show()


def coil_spidercurtext(WK,inverse):
    cname=WK+'/currents.dat'
    if inverse: cname=WK+'/currents.wr'
    lname=WK+'/coil.dat'
    fidl = open(cname, 'r')
    aa = np.array([int(x) for x in fidl.readline().split()])  # Read first line
    nl=aa[0]
    lcoils=[float(x) for x in next(fidl).split()]
    while len(lcoils) < nl :
        lcoils=np.append(lcoils,[float(x) for x in next(fidl).split()])
    fidl.close()

    fid = open(lname, 'r')
    aa = np.array([x for x in fid.readline().split()])  # Read first line
    n=int(aa[0])
    csum = 0
    csum2 = 0

    for i in range(n):
        turns = int(fid.readline().strip())  # Read turns
        aa=fid.readline().split()
        coils = np.array([float(x) for x in aa[:9]])  # Read coils
        i9 = int(coils[8]-1)
        coils[6] = 1000*lcoils[int(i9)]
        csum += abs(turns*coils[6])
        print(f'{coils[6]:.2f}',aa[9])
        
        # Plot currents in MA (this part is commented out in the original code)
        if abs(coils[6]) > 0.01 :
            #for gx,gy,name in np.broadcast(R1,Z1,name0):
            #    plt.annotate(name,(gx,gy),xytext=(gx,gy))
            # Here you would typically use a plotting library like matplotlib
            plt.annotate(f'{coils[6]:.2f}',(coils[0], coils[1]), xytext=(coils[0], coils[1]), backgroundcolor='w')

    fid.close()
    print('Sum abs currents*turns, kA:',csum)

"""
rmax = np.max(r)
rmin = np.min(r)
zmax = np.max(z)
zmin = np.min(z)

plt.figure(2)
plt.clf()
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.contour(r, z, cur, 20)
plt.plot(rm, zm, 'b+')
plt.plot(rx, zx, 'bx')
plt.plot(rmax, zmax, 'w.')
plt.plot(rmax, zmin, 'w.')
plt.plot(rmin, zmin, 'w.')
plt.plot(rmin, zmax, 'w.')
plt.plot(rk, zk, 'k+')

plt.figure(3)
plt.clf()
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.contour(r, z, ipr, 1)
plt.plot(rm, zm, 'b+')
plt.plot(rx, zx, 'bx')
plt.plot(rmax, zmax, 'w.')
plt.plot(rmax, zmin, 'w.')
plt.plot(rmin, zmin, 'w.')
plt.plot(rmin, zmax, 'w.')
plt.plot(rk, zk, 'k+')

plt.figure(4)
plt.clf()
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.contour(r, z, psie, 50)
plt.plot(rm, zm, 'y+')
plt.plot(rx, zx, 'yx')
plt.plot(rxb, zxb, 'b.')
plt.plot(rk, zk, 'k+')

plt.figure(5)
plt.clf()
plt.axis('equal')
plt.gca().set_box_aspect(1)
plt.contour(r, z, psii, 50)
plt.plot(rm, zm, 'b+')
plt.plot(rx, zx, 'bx')
plt.plot(rxb, zxb, 'b.')
plt.plot(rk, zk, 'k+')

pspl = np.zeros(ni)
psex = np.zeros(ni)
psp = np.zeros(ni)
jfi = np.zeros(ni)
for i in range(ni):
    jc = (nj + 1) // 2
    pspl[i] = psii[jc, i]
    psex[i] = psie[jc, i]
    psp[i] = psi[jc, i]
    jfi[i] = cur[jc, i]

plt.figure(6)

plt.plot(r, pspl, 'b')
plt.plot(r, psex, 'y')
plt.plot(r, psp, 'r')

plt.figure(7)
plt.plot(r, jfi, 'r.')

plt.figure(1)


vl = [psix, psix+0.001]
plt.contour(r, z, psi, vl, colors='w', linestyles=':')
plt.show()
vl = [psix + 0.001 * (psim - psix), psix + 0.001 * (psim - psix)]
cx, hx = plt.contour(r, z, psi, vl, colors='g', linestyles=':')
vl = [psib, psib]
plt.contour(r, z, psi, vl, colors='k')
vl = [psix, psix]
plt.contour(r, z, psi, vl, colors='r')
vl = [psix + 0.002 * (psim - psix), psix + 0.002 * (psim - psix)]
cx, hx = plt.contour(r, z, psi, vl, colors='g', linestyles=':')
vl = [psix + 0.003 * (psim - psix), psix + 0.003 * (psim - psix)]
cx, hx = plt.contour(r, z, psi, vl, colors='g', linestyles=':')
"""

