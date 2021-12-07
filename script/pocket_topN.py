#!/usr/bin/env python
import sys,os
import string
import subprocess
###############################################################
scriptdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(scriptdir)

BioLip = rootdir + '/BioLip/' #update 

poc_size = 'POC'
###############################################################
def bubble_sort(scorelist):
    count = len(scorelist)
    scoreindex = list()
    for i in range(count):
        scoreindex.append(i)
    
    for i in range(count):
        for j in range(i + 1, count):
            if scorelist[i] < scorelist[j]:
                scorelist[i], scorelist[j] = scorelist[j], scorelist[i]
                scoreindex[i],scoreindex[j] = scoreindex[j],scoreindex[i]
    return scorelist,scoreindex
###############################################################

fp = open(rootdir +'/user_input/results_docking/pocket/pocket_align.' + poc_size)
fpreader = fp.read()
fp.close()

fpmol2=open(rootdir +'/user_input/results_docking/pocket/' + '/pocket_topN.mol2','w')
fptop_pocket = open(rootdir +'/user_input/results_docking/pocket/pocket_topN.info','w')
pocket_information = list()
pocket_score = list()
mol2name = list()
for line in fpreader.splitlines():
    #print line
    pocket_information.append(line)
    array = line.split(',')
    pocket_score.append(float(array[1]))
    mol2name.append(array[0].split('.pdb')[0]+ '.mol2')
#print mol2name
sorted_score, sorted_index = bubble_sort(pocket_score)
#print sorted_index


if (len(sorted_score)<50):
    for ii in range(len(mol2name)):
        tmp=open(BioLip+ 'MOL2/' + mol2name[ii])
        tmpreader = tmp.read()
        #print tmpreader
        tmp.close()
        #### check the mol2 file
        checkflag = True
        atomflag = False
        bondflag = False
        atomindex = list()
        leftbondindex = list()
        rightbondindex = list()
        for mol2line in tmpreader.splitlines():
            if ("@<TRIPOS>ATOM" in mol2line):
                atomflag = True
                continue
            if("@<TRIPOS>BOND" in mol2line):
                atomflag = False
                bondflag = True
                continue
            if (atomflag == True):
                array = mol2line.split()
                atomindex.append(int(array[0]))
            if(bondflag == True):
                array=mol2line.split()
                leftbondindex.append(int(array[1]))
                rightbondindex.append(int(array[2]))
        #print (leftbondindex)
        #print (rightbondindex)
        for jj in range(len(atomindex)):

            if (atomindex[jj] not in leftbondindex and atomindex[jj] not in rightbondindex):
                checkflag = False
                print (mol2name[ii] + "  has the single atom",atomindex[jj])
                break
        if(checkflag == False):
            continue

        fpmol2.write(tmpreader)
        fptop_pocket.write(pocket_information[ii] + '\n')

if(len(sorted_score)>=50):
    coutnumber = 0
    for ii in range(len(sorted_score)):
        array = pocket_information[sorted_index[ii]].split(',')
        tmpmol2 = array[0].split('.pdb')[0]+ '.mol2'
        tmp=open(BioLip+ 'MOL2/' + mol2name[sorted_index[ii]])
        tmpreader = tmp.read()
        tmp.close()
        
        #### check the mol2 file
        checkflag = True
        atomflag = False
        bondflag = False
        atomindex = list()
        leftbondindex = list()
        rightbondindex = list()
        for mol2line in tmpreader.splitlines():
            if ("@<TRIPOS>ATOM" in mol2line):
                atomflag = True
                continue
            if("@<TRIPOS>BOND" in mol2line):
                atomflag = False
                bondflag = True
                continue
            if (atomflag == True):
                array = mol2line.split()
                atomindex.append(int(array[0]))
            if(bondflag ==True):
                array=mol2line.split()
                leftbondindex.append(int(array[1]))
                rightbondindex.append(int(array[2]))
        #print (leftbondindex)
        #print (rightbondindex)
        for jj in range(len(atomindex)):
            if (atomindex[jj] not in leftbondindex and atomindex[jj] not in rightbondindex):
                checkflag = False
                print (mol2name[ii] + "  has the single atom",atomindex[jj])
                break
        if(checkflag == False):
            continue
        fpmol2.write(tmpreader)
        
        fptop_pocket.write(pocket_information[sorted_index[ii]]+ '\n')
        coutnumber = coutnumber + 1
        if(coutnumber>=50):
            break
fpmol2.close()
fptop_pocket.close()