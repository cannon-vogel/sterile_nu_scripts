import numpy as np
import io
#import scipy
import shutil
import os
import subprocess
import sys


### Inputs
###
subfolder = 'grid_run_1' #location to put generated param files
#line 47 should be uncommented on first run to make subfolder
ms_min=0.002 #Mev 2.000e-3
ms_max=0.045 #Mev 4.500e-2
ms_sample_number=3 #int
ms_spacing=1 #1=log, 2=linear

s2_min=1.000e-14
s2_max=1.000e-7
s2_sample_number=3 #int
s2_spacing=1 #1=log, 2=linear
###
###



#create ms array
if ms_spacing == 1:
    ms_array = np.logspace(np.log(ms_min),np.log(ms_max),num=ms_sample_number,base=np.exp(1))
elif ms_spacing == 2:
    ms_array = np.linspace(ms_min,ms_max,ms_sample_number)
else:
  print("Error, choose ms_spacing either log or linear")

#create s2 array
if s2_spacing == 1:
    s2_array = np.logspace(np.log(s2_min),np.log(s2_max),num=s2_sample_number,base=np.exp(1))
elif s2_spacing == 2:
    s2_array = np.linspace(s2_min,s2_max,s2_sample_number)
else:
  print("Error, choose s2_spacing either log or linear")


#define relevant directories and create a place for new param.ini files
src_dir = os.getcwd()
dest_dir = os.mkdir(subfolder) #uncomment for first run to mkdir
dest_dir = src_dir+"/"+subfolder
print(dest_dir)
#loop to make the param.ini files and put them into the subdirectory
for i in range(ms_sample_number):
    for j in range(s2_sample_number):
    #edit the param file
        with open('params_copy.ini', 'r') as file: #data[54]=ms      data[55]=s2
            # read a list of lines into data
            data = file.readlines()

        data[54] = 'ms = '+str(np.format_float_scientific(ms_array[i],precision = 6)).replace('e', 'D')+'\n'
        data[55] = 's2 = '+str(np.format_float_scientific(s2_array[j],precision = 6)).replace('e', 'D')+'\n'
        # and write everything back
        with open('params_copy.ini', 'w') as file:
            file.writelines( data )
    #make subdirectory and copy param file into a new named file
        src_file = os.path.join(src_dir, 'params_copy.ini')
        shutil.copy(src_file,dest_dir) #copy the file to destination dir

        dst_file = os.path.join(dest_dir,'params_copy.ini')
        new_dst_file_name = os.path.join(dest_dir, 'params_'+'ms_'+str(np.format_float_scientific(ms_array[i],precision = 6)).replace('e', 'D')+'s2_'+str(np.format_float_scientific(s2_array[j],precision = 6)).replace('e', 'D')+'.ini')

        os.rename(dst_file, new_dst_file_name)#rename

#run the newly created files
for i in range(ms_sample_number):
    for j in range(s2_sample_number):
        process_test = subprocess.Popen(["./sterile-nu ./"+subfolder+'/'+'params_'+'ms_'+str(np.format_float_scientific(ms_array[i],precision = 6)).replace('e', 'D')+'s2_'+str(np.format_float_scientific(s2_array[j],precision = 6)).replace('e', 'D')+'.ini'], shell=True)
        process_test.wait()
