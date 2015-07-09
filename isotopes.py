import csv
import os
import getpass
import matplotlib.pyplot as plt
from pylab import *
import numpy as numpy
import math
import sys
from matplotlib import *
import io
from datetime import *

owd = os.getcwd()  #gets original working directory where allmol file is

#initializes lists for masses, #C, #N, #O, and #H from allmol file
masses = [] 
numC = []
numN = []
numO = []
numH = []
#lists to store unsorted data
data1 = []
txt = []

with open("allmol_sort.txt", 'rb') as f1:     #opens file and reads it in
    for i in xrange(1):
        f1.next()       #skips header at top of .txt file
    data = csv.reader(f1, delimiter='\t')
    for column in data:
        data1.append(column[0])   #adds all data from file

for i in range(0, len(data1)): #makes all data into separate numbers for list processing
    txt.append(data1[i])
newData= " ".join(txt)  
nd1 = newData.split()

"""
    Adds elements from list nd1 to a new list based on start index and step. 
    To be used to make list of masses, #C, #N, #O, #H. Step size of 5 is used
    to separate mass, C, N, O, H.
    @param list_name    name of the list to append data to
    @param start    index to start reading data from in list nd1
"""
def addToList(list_name, start):
    for i in range(start, len(nd1), 5):   
        list_name.append(nd1[i])

#adds data to lists calling addToList function
addToList(masses, 0)  
addToList(numC, 1)
addToList(numN, 2)
addToList(numO, 3)
addToList(numH, 4)

os.chdir("Mass spec data tables")  #changes directories to where file with processed RGA data is
os.chdir("Data tables 20sccm 9 torr 1")

##### Collecting masses from RGA data #####
date1 = raw_input("Enter file date (yyyy-mm-dd): ")
runNum = raw_input("Enter run number: ")
for i in os.listdir(os.getcwd()):
    if i.endswith("_peak_differences "+runNum+".txt") and i.startswith(date1):
        filename2 = i
with open(filename2) as f2: #opens RGA data file
    f2.next()
    columns = csv.reader(f2, delimiter='\t')
    mass_old = []
    intensities = []
    for i in columns:
        mass_old.append(i[0])
    nm1 = " ".join(mass_old)
    nm2 = nm1.split()
    mass_old1 = []   
    for i in range(0, len(nm2), 2):
        mass_old1.append(nm2[i])
    for i in range (1, len(nm2), 2):
        intensities.append(nm2[i])
        
os.chdir(owd) #back to original working directory (wherever allmol file is) 
                       
#### POSSIBLE MOLECULES ####

possible_mols = [] #list to store possible molecules
for i in mass_old1:
    for j in range(365): #365 is used because that is how many masses between 1 and 100 in allmol file
        if float(i)<=float(masses[j])+.5 and float(i)>=float(masses[j])-.5:
            possible_mols.append(i+ '     '+ masses[j]+'     C'+numC[j]+'N'+numN[j]+'O'+numO[j]+'H'+numH[j]) 

 ### ISOTOPES ###
abundances = [.999885, .000115, .9893, .0107, .99636, .00364, .99757, .00038, .00205]
isotopes =   ['H', 'Deuterium', 'C-12', 'C-13', 'N-14', 'N-15', 'O-16', 'O-17', 'O-18']
file_isotopes = []

def noCarbon():
    for i in possible_mols:
        if "C0" in i:
            return False
        else:
            return True
def noNitrogen():
    for i in possible_mols:
        if "N0" in i:
            return False
        else:
            return True
def noOxygen():
    for i in possible_mols:
        if "O0" in i:
            return False
        else:
            return True

def isAround(intensity1, intensity2, abundance):
    if abs(float(intensity1)*abundance) == abs(float(intensity2))+.2 or abs(float(intensity2))-.2:
        return True
    else:
        return False

for mass in mass_old1[:-1]:
    if not noCarbon():
        multiplyBy = int(float(mass)/12)
        print multiplyBy
        if (12*multiplyBy)+1 or (12*multiplyBy)+1.1 or (12*multiplyBy)+1.2 or (12*multiplyBy)+.9 in mass_old1:
            if isAround(intensities[mass_old1.index(mass)], intensities[(mass_old1.index(mass))+1], abundances[3]*multiplyBy):
                file_isotopes.append("\n" + mass + " Isotope is: " + isotopes[3])
            elif abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) <=abundances[3]*multiplyBy and abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) >= abundances[3]:
                file_isotopes.append("\n" + mass +" "+ isotopes[3] + " and another molecule (see possible molecules)")
            else:
                file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")  
        else:
            file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")
    if not noNitrogen():
        multiplyBy = int(float(mass)/14)
        print multiplyBy
        if (14*multiplyBy)+1 or (14*multiplyBy)+1.1 or (14*multiplyBy)+1.2 or (14*multiplyBy)+.9 in mass_old1:
            if isAround(intensities[mass_old1.index(mass)], intensities[(mass_old1.index(mass))+1], abundances[5]*multiplyBy):
                file_isotopes.append("\n" + mass+ " Isotope is: " + isotopes[5])
            elif abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) <=abundances[5]*multiplyBy and abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) >= abundances[5]:
                file_isotopes.append("\n" + mass +" "+ isotopes[5] + " and another molecule (see possible molecules)")    
            else:
                file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")
        else:
            file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")
    if not noOxygen():
        multiplyBy = int(float(mass)/16)
        print multiplyBy
        if (16*multiplyBy)+1 or (16*multiplyBy)+1.1 or (16*multiplyBy)+1.2 or (16*multiplyBy)+.9 in mass_old1:
            if isAround(intensities[mass_old1.index(mass)], intensities[(mass_old1.index(mass))+1], abundances[7]*multiplyBy):
                file_isotopes.append("\n" + mass+ " Isotope is: " + isotopes[7])
            elif abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) <=abundances[7]*multiplyBy and abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) >= abundances[7]:
                file_isotopes.append("\n" + mass +" "+ isotopes[7] + " and another molecule (see possible molecules)") 
            else:
                file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")   
        if (16*multiplyBy)+2 or (16*multiplyBy)+2.1 or (16*multiplyBy)+2.2 or (16*multiplyBy)+1.9 in mass_old1:
            if isAround(intensities[mass_old1.index(mass)], intensities[(mass_old1.index(mass))+1], abundances[8]*multiplyBy):
                file_isotopes.append("\n" + mass + " Isotope is: " + isotopes[8])
            elif abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) <=abundances[8]*multiplyBy and abs(intensities[(mass_old1.index(mass))+1]/intensities[mass_old1.index(mass)]) >= abundances[8]:
                file_isotopes.append("\n" + mass +" "+ isotopes[8] + " and another molecule (see possible molecules)")
            else:
                file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")
        else:
            file_isotopes.append("\n" + mass + " Another molecule (see possible molecules)")  

#### FILE CREATION ####
#creates new file with possible molecular weights and formulas for given RGA mass
username = getpass.getuser()  #gets username for computer   
os.chdir('/Users/'+username+'/Desktop') #change directory to desktop
        
#Make new folder on desktop if folder name not already taken, otherwise don't and move on
try:
    os.mkdir('Isotopes and possible molecules')
except:
    pass 
os.chdir('Isotopes and possible molecules')

name = (date1 + "_possible_mols_"+ runNum+".txt")  #output file name is based on input peak differences file
w = open(name, 'w')
w.write("RGA Mass |  MW     | Formula\n")
for i in possible_mols:
    w.writelines("%s\n" % i)
for j in file_isotopes:
    w.writelines("%s\n" % j)
w.close()  


#### GRAPH #####                       
"""given_masses1 = raw_input("Enter the masses you would like isotopes for, separated by commas: ")
new_gm= "".join(given_masses1)  
given_masses = new_gm.split(",")
print given_masses
                    """   
  
                                            
print "\nProgram ended"
os.chdir(owd)
