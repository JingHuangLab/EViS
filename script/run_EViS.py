#!/usr/bin/env python
import sys,os
import string
import subprocess
import time
scriptdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(scriptdir)
BioLip = rootdir + '/BioLip/'

#### step 1: ppsalign
print ("step1/4 run PPS-align")
command= scriptdir + '/ppsalign.py'
stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()


#### step 2: ranking and select the maximum 50 templates
print ("step2/4 run ranking and select the maximum 50 templates")
command= scriptdir + '/pocket_topN.py'
stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()

command = 'cp ' + rootdir +'/user_input/results_docking/pocket/pocket_topN* ' + rootdir +'/user_input/results_docking/ligands_mol2/'
stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()


#### step 3: LS-align
print ("step3/4 run LS-align")

command1 = 'cd ' + rootdir +'/user_input/results_docking/ligands_mol2/'

total_mol2 = list()
lsalign_index = 0
for mol2_item in (os.listdir(rootdir +'/user_input/results_docking/ligands_mol2/')):
    if ('pocket_topN.mol2' in mol2_item):
        continue
    if '.mol2' in mol2_item :
        total_mol2.append(mol2_item)

for ii in range(len(total_mol2)):
    lsalign_index = lsalign_index + 1
    print ('LSalign ' + total_mol2[ii] + ' ----' + str(lsalign_index) + '/' + str(len(total_mol2)))
    command2 = scriptdir + '/LSalignO pocket_topN.mol2 ' + total_mol2[ii] + ' >' + total_mol2[ii].split('.mol2')[0]+'.lsalign'
    stdout,stderr = subprocess.Popen(';'.join([command1, command2]),shell=True).communicate() 

#### step 4: PL-score
print ("step4/4 run PL-score")
command= scriptdir + '/PLscore.py'
stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()
