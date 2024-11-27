# astra_smart: part of ASTRA workflow for SMART tokamak

 astra_core -- astra_smart -- astra_user

 astra_smart is the place of all ASTRA stuff we have for SMART tasks


## Installing Astra-Spider with TE specific (astra_core -- astra_smart -- astra-user)
```
mkdir ~/SMART
cd  ~/SMART 
git clone ssh://git@tokamak-devlin.tokamak.local:5740/physics/astra_smart.git
module load intel-compilers/2021.1.2
module unload GCCcore/10.2.0 zlib/1.2.11-GCCcore-10.2.0 binutils/2.35-GCCcore-10.2.0
tepm.py --conf_root=astra_smart spider
make -C spider/ -f Makefile_intel
tepm.py --conf_root=astra_smart astra_core
mv astra_core/Astra Astra
./astra_core/bin_grp/MAKER Astra Intel
./astra_smart/MAKER_SMART . astra_smart Intel
./astra_core/bin_grp/MAUSER Astra astra_user Intel
./astra_smart/MAUSER_SMART . astra_smart astra_user Intel
```
### Standart ASTRA test
```
cd astra_user
.exe/astra readme showdata
```
Note that the above test has a netcdf dependency. Please see instructions below and check your LD_LIBRARY_PATH environment variable.

## Enabling data-visualisation in Astra-Spider with netcdf.
For Centos7, get the libraries like this:
```
cd  ../
tepm.py --conf_root=astra_smart centos7_dev
LD_LIBRARY_PATH=$(pwd)/centos7_dev/opt/lib:$LD_LIBRARY_PATH
```
## Using panels for data processing install python GUI library 
```
pip3 install -Iv PySimpleGUI==4.60.5
```
 Then run main panel
```
python3 pyt/panel_all.py
```

## Test for SMART plasma with prescribed boundary

```
.exe/astra smart_test1 smart_fixed 0 0.4 smart_test1

```
## Test for vacuum phase for SMART

```
.exe/astra smart_fb_test1 smart_vac 0 0.01 smart_test2

```

# interface to SOPHIA


## SOPHIA (latest version is under development and is not fully tested!!!)

Latest SOPHIA that was tested and can be made to work is tagged and released under 1.0.0_alpha
A stabled more ironed-out release is to follow.

go with installing Astra-Spider with TE specific (astra_core -- astra_smart -- astra-user) and the continue to install SOPHIA

```
git clone ssh://git@tokamak-devlin.tokamak.local:5740/st40/ops/sophia.git
tepm.py --conf_root=sophia pcs pfit mds_trees
tepm.py --build_all --conf_root=pcs yq mds_corrected
make -C sophia/models/${model_name} -f Makefile smlk
make -C sophia/models/${model_name} -f Makefile fortran
./sophia/bash_scripts/setenv_interface_so.sh ./astra_user/.exe/astrarc ../sophia/models/st40_pfit/bin
cp sophia/models/st40_pfit/m-files/personal_setup_template.m sophia/models/st40_pfit/m-files/personal_setup.m
./sophia/bash_scripts/set_pulse_range your_pulse_range
```
Then go with SOPHIA project taking in mind that INSTALL.sh command is already done.

* ASTRA models tested to work in SOPHIA: 
* st40_smlnk_vac - vacuum case only
* st40_smlnk_ts_fb - run w/o NUBEAM
* nust40_smlnk_ts_fb - run with NUBEAM

Interface to SOPHIA is done.




