#!/usr/bin/env python
import sys,os
import string
import subprocess
import time
jobname = sys.argv[1]
scriptdir=os.path.dirname(os.path.abspath(__file__))
rootdir=os.path.dirname(scriptdir)
#print (rootdir)
os.mkdir(rootdir + '/output/')

virtualflow_original_dir=rootdir+'/library/virtualflow_original/'
virtualflow_new_dir = rootdir + '/output/' + jobname + '/'
user_input_folder = rootdir + '/user_input/virtualflow_prepare/'


#### step 1: mkdir virtualflow folder 
#print scriptdir
command1 =  'mkdir ' + virtualflow_new_dir
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'mkdir ' + virtualflow_new_dir + 'input-files'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'mkdir ' + virtualflow_new_dir + 'input-files/ligand-library'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'mkdir ' + virtualflow_new_dir + 'input-files/ligand-library/AA/'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'mkdir ' + virtualflow_new_dir + 'input-files/ligand-library/AA/AABBCC/'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
#### step 2: copy tools and user input folder: qvina02_rigid_receptor1, receptor  
#print scriptdir
command1 =  'cp -r ' + virtualflow_original_dir + '/tools/ ' + virtualflow_new_dir
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'cp -r ' + user_input_folder + 'qvina02_rigid_receptor1/ ' +  virtualflow_new_dir + '/input-files/'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()
command1 =  'cp -r ' + user_input_folder + 'receptor/ ' +  virtualflow_new_dir + '/input-files/'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()

#### step 3: generate the subfolders in '/input-files/ligand-library/AA/AABBCC/'
pdbqtlist = list() 
folderindex=0
fp_todo = open('todo.all','w')
for item in os.listdir(user_input_folder+'/ligands_input/'):
    if ('.pdbqt' in item):
        pdbqtlist.append(item)  
for j in range(0,len(pdbqtlist)):
    if((j)%1000==0):
        if (not os.path.exists(virtualflow_new_dir + '/input-files/ligand-library/AA/AABBCC/'+str("%05d" % folderindex)+'/')):
            os.mkdir(virtualflow_new_dir + '/input-files/ligand-library/AA/AABBCC/'+str("%05d" % folderindex)+'/')
        if ((folderindex+1)*1000<=len(pdbqtlist)): 
            #print jobname + '_' + str(("%05d" % folderindex)) + ' ' + str(1000)
            print 'AABBCC' + '_' + str(("%05d" % folderindex)) + ' ' + str(1000)
            fp_todo.write('AABBCC' + '_' + str(("%05d" % folderindex)) + ' ' + str(1000)+'\n')
        else:
            #print jobname + '_' + str(("%05d" % folderindex)) + ' ' + str(len(pdbqtlist) - (folderindex)*1000)
            print 'AABBCC' + '_' + str(("%05d" % folderindex)) + ' ' + str(len(pdbqtlist) - (folderindex)*1000)
            fp_todo.write('AABBCC' + '_' + str(("%05d" % folderindex)) + ' ' + str(len(pdbqtlist) - (folderindex)*1000)+'\n')
        foldername = str("%05d" % folderindex)
        folderindex = folderindex + 1
        #print foldername 
    command = 'cp ' + user_input_folder + '/ligands_input/'  + pdbqtlist[j] + ' ' + virtualflow_new_dir + '/input-files/ligand-library/AA/AABBCC/'+str("%05d" % (folderindex-1))+'/'
    #print command
    stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()
fp_todo.close()


#### step 4: tar 
for ii in range(folderindex):

    command1 = 'cd ' + virtualflow_new_dir + 'input-files/ligand-library/AA/AABBCC/'
    command2 = 'tar -cvzf '  + str("%05d" % ii) + '.tar.gz ' + str("%05d" % ii) 
    stdout,stderr = subprocess.Popen(';'.join([command1,command2]),shell=True).communicate()

    command1 = 'rm -r ' + virtualflow_new_dir + 'input-files/ligand-library/AA/AABBCC/' + str("%05d" % ii) 
    stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()

command1 = 'cd ' + virtualflow_new_dir + 'input-files/ligand-library/AA/'
command2 = 'tar -cvf AABBCC.tar AABBCC'
stdout,stderr = subprocess.Popen(';'.join([command1,command2]),shell=True).communicate()

command1 = 'rm -r ' + virtualflow_new_dir + 'input-files/ligand-library/AA/AABBCC/'
stdout,stderr = subprocess.Popen(';'.join([command1]),shell=True).communicate()

#### step 5: run virtualflow

command = 'cp todo.all ' + virtualflow_new_dir + 'tools/templates/'
stdout,stderr = subprocess.Popen(';'.join([command]),shell=True).communicate()
fp=open(virtualflow_new_dir+'tools/templates/template3.slurm.sh','r')
fpreader = fp.read()
fp.close()
fpout = open(virtualflow_new_dir+'tools/templates/template4.slurm.sh','w')
for line in fpreader.splitlines():
    if ('export VF_JOBLETTER=' in line):
        #print line
        fpout.write('export VF_JOBLETTER=\"' +str(jobname)+ '\"\n')
        continue
    else:
        fpout.write(line+ '\n')
fpout.close()

command1 = 'cd ' + virtualflow_new_dir + 'tools'
command2 = './vf_prepare_folders.sh '
command3 = './vf_start_jobline.sh 1 2 ./templates/template4.slurm.sh submit 1 '
stdout,stderr = subprocess.Popen(';'.join([command1,command2,command3]),shell=True).communicate()




