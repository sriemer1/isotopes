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
file_isotopes = []  #to store the isotopes to put into the file

isotope_masses1=[]
for element in possible_mols[2:]:
  isotope_masses1.append(element[0:5]) 
isotope_masses = [float(i) for i in isotope_masses1]
print isotope_masses

molecules = []
for element in possible_mols[2:]:
    molecules.append(element[24:])
   
def noCarbon(molecule):
    for molecule in molecules:
        if 'C0' in molecule:
            return True
        else:
            return False
            
def noNitrogen(molecule):
    for molecule in molecules:
        if 'N0' in molecule:
            return True
        else:
            return False
            
def noOxygen(molecule):
    for molecule in molecules:
        if 'O0' in molecule:
            return True
        else:
            return False

def isAround(intensity1, intensity2, abundance):
    if abs(float(intensity1)*abundance) == abs(float(intensity2))+.000000005 or abs(float(intensity2))-.000000005:
        return True
    else:
        return False

def getMassPlus(mass):
        if mass+1 in isotope_masses:
            return mass+1
        elif mass+1.1 in isotope_masses:
            return mass+1.1
        elif mass+1.2 in isotope_masses:
            return mass+1.2
        elif mass+.9 in isotope_masses:
            return mass+.9

def getMassPlusTwo(mass):
    if mass+2 in isotope_masses:
        return mass+2
    elif mass+2.1 in isotope_masses:
        return mass+2.1
    elif mass+2.2 in isotope_masses:
        return mass+2.2
    elif mass+1.9 in isotope_masses:
        return mass+1.9

def hasDoubleDig(element):
    if element == 'C':
        if type(int(molecules[i][1:3])) is int:
            return True
        else:
            return False
    elif element == 'N':
        if type(int(molecules[i][3:5])) is int:
            return True
        else:
            return False
    elif element == 'O':
        if type(int(molecules[i][5:7])) is int:
            return True
        else:
            return False
             
for i in range(len(isotope_masses)):
    if not noCarbon(molecules[i]) and not noNitrogen(molecules[i]) and not noOxygen(molecules[i]):
        #gets number of atoms of each element
        if hasDoubleDig('C'):
            multiplyByC = int(molecules[i][1:3])
            if hasDoubleDig('N'):
                multiplyByN = int(molecules[i][4:6])
                if hasDoubleDig('O'):
                    multiplyByO = int(molecules[i][7:9])
                    multiplyByH = int(molecules[i][9:])
                else:
                    multiplyByO = int(molecules[i][7])
                    multiplyByH = int(molecules[i][8:])
            else:
                multiplyByN = int(molecules[i][4])
        else:
            multiplyByC = int(molecules[i][1])
            if hasDoubleDig('N'):
                multiplyByN = int(molecules[i][3:5])
                if hasDoubleDig('O'):
                    multiplyByO = int(molecules[i][6:8])
                    multiplyByH = int(molecules[i][9:])
                else:
                    multiplyByO = int(molecules[i][6])
                    multiplyByH = int(molecules[i][8:])
            else:
                multiplyByN = int(molecules[i][3])
                if hasDoubleDig('O'):
                    multiplyByO = int(molecules[i][5:7])
                    multiplyByH = int(molecules[i][8:])
                else:
                    multiplyByO = int(molecules[i][5])
                    multiplyByH = int(molecules[i][7:])
        #check to see if molecular mass equals a mass from RGA data
        if ((12.0107*multiplyByC)+(14.00674*multiplyByN)+(15.994915*multiplyByO)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:  #checks to see if mass+1 is in RGA data
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByC * .0107:
                    file_isotopes.append("Isotope is: C-13")
                elif intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByN * .00364:
                    file_isotopes.append("Isotope: is N-15")
                elif intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00038:
                    file_isotopes.append("Isotope is: O-17")
                else:
                    file_isotopes.append("Mix of isotopes")
            if isotope_masses[i]+2 or isotope_masses[i]+2.1 or isotope_masses[i]+2.2 or isotope_masses[i]+1.9 in mass_old1: #separate check for O-18 isotope, checks mass+2
                nextMassTwo = getMassPlusTwo(isotope_masses[i])
                if intensities[mass_old1.index(nextMassTwo)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00205:
                    file_isotopes.append("Isotope is: O-18")
                else:
                    file_isotopes.append("Mix of isotopes")
                    
    elif not noCarbon(molecules[i]) and not noNitrogen(molecules[i]):
        multiplyByC = int(molecules[i][1])
        multiplyByN = int(molecules[i][3])
        multiplyByH = int(molecules[i][7:])
        if ((12.0107*multiplyByC)+(14.00674*multiplyByN)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByC * .0107:
                    file_isotopes.append("Isotope is: C-13")
                elif intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByN * .00364:
                    file_isotopes.append("Isotope: is N-15")
                else:
                    file_isotopes.append("Mix of isotopes")
                    
    elif not noNitrogen(molecules[i]) and not noOxygen(molecules[i]):
        multiplyByN = int(molecules[i][3])
        multiplyByO = int(molecules[i][5])
        multiplyByH = int(molecules[i][7:])
        if ((14.00674*multiplyByN)+(15.994915*multiplyByO)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5: 
          if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:
            nextMass = getMassPlus(isotope_masses[i])
            if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByN * .00364:
                file_isotopes.append("Isotope: is N-15")
            elif intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00038:
                file_isotopes.append("Isotope is: O-17")  
            else:
                file_isotopes.append("Mix of isotopes")
          if isotope_masses[i]+2 or isotope_masses[i]+2.1 or isotope_masses[i]+2.2 or isotope_masses[i]+1.9 in mass_old1:
              nextMassTwo = getMassPlusTwo(isotope_masses[i]) 
              if intensities[mass_old1.index(nextMassTwo)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00205:
                  file_isotopes.append("Isotope is: O-18")
              else:
                  file_isotopes.append("Mix of isotopes")
                  
    elif not noCarbon(molecules[i]) and not noOxygen(molecules[i]):
        multiplyByC = int(molecules[i][1])
        multiplyByO = int(molecules[i][5])
        multiplyByH = int(molecules[i][7:])
        if ((12.0107*multiplyByC)+(15.994915*multiplyByO)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:  
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByC * .0107:
                    file_isotopes.append("Isotope is: C-13")
                elif intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00038:
                    file_isotopes.append("Isotope is: O-17")
                else:
                  file_isotopes.append("Mix of isotopes")
            if isotope_masses[i]+2 or isotope_masses[i]+2.1 or isotope_masses[i]+2.2 or isotope_masses[i]+1.9 in mass_old1:
                nextMassTwo = getMassPlusTwo(isotope_masses[i])
                if intensities[mass_old1.index(nextMassTwo)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00205:
                    file_isotopes.append("Isotope is: O-18")
                else:
                    file_isotopes.append("Mix of isotopes")   
                       
    elif not noCarbon(molecules[i]):
        multiplyByC = int(molecules[i][1])
        multiplyByH = int(molecules[i][7:])
        if ((12.0107*multiplyByC)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByC * .0107:
                    file_isotopes.append("Isotope is: C-13")
                else:
                    file_isotopes.append("Mix of isotopes")
       
    elif not noNitrogen(molecules[i]):
        multiplyByN = int(molecules[i][3])
        multiplyByH = int(molecules[i][7:])
        if ((14.00674*multiplyByN)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByN * .00364:
                    file_isotopes.append("Isotope: is N-15") 
                else:
                    file_isotopes.append("Mix of isotopes")   
            
    elif not noOxygen(molecules[i]):
        multiplyByO = int(molecules[i][5])
        multiplyByH = int(molecules[i][7:])
        if ((15.994915*multiplyByO)+(1.00794*multiplyByH)) == isotope_masses[i]+.5 or isotope_masses[i]-.5:
            if isotope_masses[i]+1 or isotope_masses[i]+1.1 or isotope_masses[i]+1.2 or isotope_masses[i]+.9 in mass_old1:
                nextMass = getMassPlus(isotope_masses[i])
                if intensities[mass_old1.index(nextMass)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00038:
                    file_isotopes.append("Isotope is: O-17")
                else:
                  file_isotopes.append("Mix of isotopes")
            if isotope_masses[i]+2 or isotope_masses[i]+2.1 or isotope_masses[i]+2.2 or isotope_masses[i]+1.9 in mass_old1: 
                nextMassTwo = getMassPlusTwo(isotope_masses[i])
                if intensities[mass_old1.index(nextMassTwo)]/intensities[mass_old1.index(isotopes_masses[i])] == multiplyByO * .00205:
                    file_isotopes.append("Isotope is: O-18")
                else:
                    file_isotopes.append("Mix of isotopes")

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
