#!/usr/bin/env python
import sys,os
import string
import subprocess

###############################################################
scriptdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(scriptdir)
outputdir = rootdir + '/user_input/results_docking/pocket/'

BioLip = rootdir + '/BioLip/'

poc_size = 'POC'

###############################################################
#print (os.listdir(rootdir+'/user_input/results_docking/pocket/')
for ii in os.listdir(rootdir+'/user_input/results_docking/pocket/'):
    if ('.poc' in ii):
        pocketname = str(ii)
        break
targetname = pocketname.split('.poc')[0]
print (pocketname)

fp = open('pocket_num','r')
fpreader = fp.read()
fp.close()

pocket_information = list()
flagindex = 0
template_num  = len(fpreader.splitlines())
for line in fpreader.splitlines():
    flagindex = flagindex + 1
    array = line.split()
    templateligand = array[0]
    templatepoc = array[0].split('.mol2')[0] + '.pdb'
    command1 = 'cd ' + outputdir
    command2 = scriptdir + '/PPSalign ' + pocketname + ' ' + BioLip+ str(poc_size) + '/' + templatepoc + ' >align_info'+ '_' + poc_size
    stdout,stderr = subprocess.Popen(';'.join([command1,command2]),shell=True).communicate() 
    
    falign = open(outputdir + '/align_info_' + poc_size,'r')
    align_reader = falign.read()
    falign.close()
    
    tmp_score=0.0
    tmp_query_aa = ''
    tmp_templ_aa = ''
    for align_line in align_reader.splitlines():   
        if targetname in align_line:
            #print align_line
            tmp_score = float(align_line.split()[2])
            #print flagindex,tmp_score
            continue
        if 'Query AA Index:' in align_line:
            tmp_query_aa = align_line.split(':')[1]
            continue
        if 'Templ AA Index:' in align_line:
            tmp_templ_aa = align_line.split(':')[1]
            break
    print (str(flagindex)+ '/' + str(template_num)+ '\t' + templatepoc+'\t'+str(tmp_score))
    if(tmp_score>=0.5):
        pocket_information.append(templatepoc+',' +str(tmp_score)+','+tmp_query_aa+','+tmp_templ_aa)
        print (templatepoc+',' +str(tmp_score)+','+tmp_query_aa+','+tmp_templ_aa,'#', flagindex)
        
fpout = open(outputdir + '/pocket_align.' + poc_size,'w')
for letter in pocket_information:
    fpout.write(letter+'\n')
fpout.close()
