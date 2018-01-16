#!/usr/bin/python
#
#
#(c) 2017 Adewale Amosu
#
#
###############################

import xlrd
import sys
import numpy as np
import os
import mmap
import pprint
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import MultipleLocator
import re

##############################
print " "
print " ------------------------------------------------------------------------------------------------"
print "  PyLogFinder.py: Program to check if specific logs are in multiple LAS files using any Mnemonic "
print "  (c) 2017 Authors: Adewale Amosu, Hamdi Mahmood"
print "  Texas A&M University"
print " ------------------------------------------------------------------------------------------------"
print " "
print "   Number of arguments: ", len(sys.argv)
print " "
print "   The arguments are: " , str(sys.argv)
print " "


if len(sys.argv) <=1:
   print " ------------------------------------------------------------------------------------------------"
   print " "
   print "   Usage: python PyLogFinder.py Foldername_containing_LAS_files, List_of_Mnemonics_separated_by_commas"
   print " "
   print "   e.g: python PyLogFinder.py TEST_DATA,DT,DTS,GR,LLD,PE"
   print " "
   print "   See 'Database.xls' for full list of Mnemonics or to add new Mnemonics"
   print " "
   print " ------------------------------------------------------------------------------------------------"
   sys.exit(1)

strval2 = sys.argv[1].split(',')
strval=strval2[1:]
#print strval

if len(strval2) <2:
   print " ------------------------------------------------------------------------------------------------"
   print " "
   print "   Usage: python PyLogFinder.py Foldername_containing_LAS_files, List_of_Mnemonics_separated_by_commas" 
   print " "
   print "   e.g: python PyLogFinder.py TEST_DATA,DT,DTS,GR,LLD,PE"
   print " "
   print "   See 'Database.xls' for full list of Mnemonics or to add new Mnemonics"
   print " "
   print " ------------------------------------------------------------------------------------------------"
   sys.exit(1)


###############################
## folder,store files in array
#
foldername=strval2[0]
print "   FolderName:", foldername
print " "

dirlist=os.listdir(foldername)
files=[]
for filename in dirlist:
    if ".LAS" in filename:
       files.append('./'+foldername+'/'+filename)
for filename in dirlist:
    if ".las" in filename:
       files.append('./'+foldername+'/'+filename)
## print files   
##############################


##############################
#Extract from  Database
#
data = xlrd.open_workbook('Database.xls')
sheetname = data.sheet_names()
logall = data.sheet_by_index(0)

valMN = [c.value for c in logall.col(0)]
valTY = [c.value for c in logall.col(2)]
valUN = [c.value for c in logall.col(3)]
valDE = [c.value for c in logall.col(4)]
#Print Data
#for k in range(0, len(valMN)):
#    print valMN[k]," : ", valTY[k]," : ", valDE[k]
#############################


##############################
# index2checkm 
inputind = []
checkm =[]
for k in range(0, len(strval)):
    inputind.append(valMN.index(strval[k]))
    ind1 = valMN.index(strval[k])
    checkm.append((valTY[ind1]))
    print "  ", strval[k], inputind[k], checkm[k]
##############################



#############################
# Extract Mnemonics, grep in file, results store in 2D array
#results = [[0 for _ in range(0, len(files))] for _ in range(0, len(checkm))]
#pprint.pprint(results)
results=np.zeros(shape=(len(files), len(checkm)))
#pprint.pprint(results)

for j in range(0, len(files)):
    print "  ------------------------------------------------------"
    for k in range(0, len(checkm)):
       print " "
       indices = [i for i, x in enumerate(valTY) if x == checkm[k]]
       grepL = np.array(valMN)[indices]
       #print checkm[k], indices
       for mnem in grepL:
          #if mnem+'.' in open(files[j]).read():
          f = open(files[j])
          s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
          #if s.find(mnem) != -1:
          if re.search(r'\b' + mnem + r'\b', s):
             results[j][k]=1
             print "   ",j,k, files[j], mnem, results[j][k]
             break
             
#pprint.pprint(results)

#############################
# print result to screen and files
f = open(foldername+"_Results.txt",'w')
print "   "
sys.stdout.write("   ")
sys.stdout.write("Files ")
f.write("Files ")
for k in range(0, len(strval)):
    sys.stdout.write(strval[k]+" ")
    f.write(strval[k]+" ")
print " "
f.write('\n')
for j in range(0, len(files)):
    #print(files[j], " ", end='')
    sys.stdout.write("   ")
    sys.stdout.write(files[j])
    sys.stdout.write(" ")
    f.write(str(files[j]))
    f.write(" ")
    for k in range(0, len(checkm)):
        #print results[j, k]
        sys.stdout.write("   ")
        sys.stdout.write("%d " % (results[j,k]))
        sys.stdout.write("   ")
        f.write(str(results[j,k]))
        f.write(" ")
    print " "
    f.write('\n')

f.close()



##################################
#Plots
row_labels=files
col_labels=strval
cmap = colors.ListedColormap(['white', 'springgreen'])
#cmap = colors.ListedColormap(['white', 'red'])
fig, ax = plt.subplots(figsize=(25, 15)) 
ax.imshow(results, cmap=cmap, interpolation='nearest', aspect='auto')
ax.grid(which='minor', linestyle='-', linewidth=2,alpha=1)
ax.xaxis.set_ticks_position("top")

plt.rc('font', size=23) 
plt.xticks(range(0, len(strval)), col_labels)
plt.yticks(range(0, len(files)), row_labels)
locs = np.arange(len(row_labels))
for axis in [ax.yaxis]:
    axis.set_ticks(locs + 0.5, minor=True)
    axis.set(ticks=locs)
locs = np.arange(len(col_labels))
for axis in [ax.xaxis]:
    axis.set_ticks(locs + 0.5, minor=True)
    axis.set(ticks=locs)
ax.grid(True, which='minor')
plt.gca().set_position([0.25, 0.2, 0.65, 0.7])
#
#save and display
plt.savefig(foldername+"_Results.png")
plt.show()
