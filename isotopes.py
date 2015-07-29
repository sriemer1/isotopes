import csv
import os
import getpass
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pylab import *
import numpy as numpy
import math
import sys
from matplotlib import *
import io
from datetime import *

owd = os.getcwd()  #gets original working directory where allmol file is

#initializes lists for masses, #C, #N, #O, and #H from allmol file
masses, numC, numN, numO, numH, data1, txt = ([] for i in range(7))

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

def addToList(list_name, start):
    """
    Adds elements from list nd1 to a new list based on start index and step. 
    To be used to make list of masses, #C, #N, #O, #H. Step size of 5 is used
    to separate mass, C, N, O, H. Takes parameters list_name, name of the list to append data to
    and start, index to start reading data from in list nd1
    """
    for i in range(start, len(nd1), 5):   
        list_name.append(nd1[i])

#adds data to lists calling addToList function
addToList(masses, 0)  
addToList(numC, 1)
addToList(numN, 2)
addToList(numO, 3)
addToList(numH, 4)

os.chdir("Mass spec data tables")  #changes directories to where file with processed RGA data is
flow = raw_input("Enter flow rate: ")
torr = raw_input("Enter torr: ")
runNum = raw_input("Enter run number: ")
os.chdir("Data tables "+ flow+"sccm "+ torr+" torr "+runNum)

##### Collecting masses from RGA data #####
date1 = raw_input("Enter file date (yyyy-mm-dd): ")
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
mass_old2 = [float(i) for i in mass_old1]    
        
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
            
def getMassPlus(mass):
    """
    Gets the mass that may have an isotope of +1 neutron for 
    C,N or O (if there is one).Takes parameter mass, the mass 
    you want to check if there is data for and returns the mass +1.
    """
    if mass+1 in mass_old2:
        return mass+1
    elif mass+1.1 in mass_old2:
        return mass+1.1
    elif mass+1.2 in mass_old2:
        return mass+1.2
    elif mass+.9 in mass_old2:
        return mass+.9
    elif mass+.8 in mass_old2:
        return mass+.8

def getMassPlusTwo(mass):
    """
    Gets the mass that may have an isotope of +2 neutron for 
    O (if there is one).Takes parameter mass, the mass you 
    want to check data for  and returns the mass+2.
    """
    if mass+2 in mass_old2:
        return mass+2
    elif mass+2.1 in mass_old2:
        return mass+2.1
    elif mass+2.2 in mass_old2:
        return mass+2.2
    elif mass+1.9 in mass_old2:
        return mass+1.9
    elif mass+1.8 in mass_old2:
        return mass+1.8

def hasDoubleDig(element):
    """
    Checks if the number of carbons, nitrogens or oxygens is in double-digits.
    Takes parameter element, the element to check quantity of.
    Returns 'True' if there are >9 of an element in a molecule, 'False' otherwise.
    """
    if element == 'C':
        try:
            int(molecules[i][1:3])
            return True
        except:
            return False
    elif element == 'N':
        try:
            int(molecules[i][3:5])
            return True
        except:
            return False
    elif element == 'O':
        try:
            int(molecules[i][5:7])
            return True
        except:
            return False

isotope_masses1=[]
for element in possible_mols[2:]:
  isotope_masses1.append(element[0:5]) 
isotope_masses = [float(i) for i in isotope_masses1] #list to store masses that have corresponding possible molecules

molecules = []  #list to store the possible molecules
for element in possible_mols[2:]:
    molecules.append(element[24:])  
             
for i in range(len(isotope_masses)):
    #if not noCarbon(molecules[i]) and not noNitrogen(molecules[i]) and not noOxygen(molecules[i]): #molecule has C,N,O and possibly H
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
    if ((12.0107*multiplyByC)+(14.00674*multiplyByN)+(15.994915*multiplyByO)+(1.00794*multiplyByH)) <= isotope_masses[i]+.5 and ((12.0107*multiplyByC)+(14.00674*multiplyByN)+(15.994915*multiplyByO)+(1.00794*multiplyByH)) >= isotope_masses[i]-.5:
        if isotope_masses[i]+1 in mass_old2 or isotope_masses[i]+1.1 in mass_old2 or isotope_masses[i]+1.2 in mass_old2 or isotope_masses[i]+.9 in mass_old2 or isotope_masses[i]+.8 in mass_old2:  #checks to see if mass+1 is in RGA data
            nextMass = getMassPlus(isotope_masses[i])
            #checks if the ratio of the intensities equals the isotope abundance
            if float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) <= (multiplyByC * .0107)+.001 and float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) >= (multiplyByC * .0107)-.001:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Isotope is: C-13")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
            elif float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) <= (multiplyByN * .00364)+.0001 and float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) >= (multiplyByN * .00364)-.0001:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Isotope: is N-15")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
            elif float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) <= (multiplyByO * .00038)+.00001 and float(intensities[mass_old2.index(nextMass)])/float(intensities[mass_old2.index(isotope_masses[i])]) >= (multiplyByO * .00038)-.00001:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Isotope is: O-17")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
            else:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Mix of isotopes and/or molecules")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
        if isotope_masses[i]+2 in mass_old2 or isotope_masses[i]+2.1 in mass_old2 or isotope_masses[i]+2.2 in mass_old2 or isotope_masses[i]+1.9 in mass_old2 or isotope_masses[i]+1.8 in mass_old2: #separate check for O-18 isotope, checks mass+2
            nextMassTwo = getMassPlusTwo(isotope_masses[i])
            if float(intensities[mass_old2.index(nextMassTwo)])/float(intensities[mass_old2.index(isotope_masses[i])]) <= (multiplyByO * .00205)+.0001 and float(intensities[mass_old2.index(nextMassTwo)])/float(intensities[mass_old2.index(isotope_masses[i])]) >= (multiplyByO * .00205)-.0001:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Isotope is: O-18")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
            else:
                file_isotopes.append(str(nextMass)+"/"+str(isotope_masses[i]) + " Mix of isotopes and/or molecules")
                file_isotopes.append(molecules[i])
                file_isotopes.append("------------")
                    
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
w.write("\nISOTOPES\n\n")
for j in file_isotopes:
    w.writelines("%s\n" % j)
w.close()  

##### GRAPH #####

def isMatch(filename, mass):
    """
    Finds the file that has the data for the molecule with the given mass.
    Takes parameter filename, the name of the file being evaluated for mass
    and param mass, the target mass. Returns 'True' if file molecular mass 
    corresponds to given mass, 'False' otherwise.
    """
    totalMass = 0
    if 'H' in filename:
        if filename[filename.index('H')+1].isdigit() and filename[filename.index('H')+2].isdigit():
            H = int(filename[filename.index('H')+1:filename.index('H')+2])
            totalMass+=(1*H)
        elif filename[filename.index('H')+1].isdigit():  
            H = int(filename[filename.index('H')+1])
            totalMass+=(1*H)
        else:
            totalMass+=1
            
    if 'N' in filename:
        if filename[filename.index('N')+1].isdigit() and filename[filename.index('N')+2].isdigit():
            N = int(filename[filename.index('N')+1:filename.index('N')+2])
            totalMass+=(14*N)
        elif filename[filename.index('N')+1].isdigit():  
            N = int(filename[filename.index('N')+1])
            totalMass+=(14*N)
        else:
            totalMass+=14
        
    if 'C' in filename:
        if filename[filename.index('C')+1].isdigit() and filename[filename.index('C')+2].isdigit():
            C = int(filename[filename.index('C')+1:filename.index('C')+2])
            totalMass+=(12*N)
        elif filename[filename.index('C')+1].isdigit():  
            C = int(filename[filename.index('C')+1])
            totalMass+=(12*C)
        else:
            totalMass+=12
            
    if 'O' in filename:
        if filename[filename.index('O')+1].isdigit() and filename[filename.index('O')+2].isdigit():
            O = int(filename[filename.index('O')+1:filename.index('O')+2])
            totalMass+=(16*O)
        elif filename[filename.index('O')+1].isdigit():  
            O = int(filename[filename.index('O')+1])
            totalMass+=(16*O)
        else:
            totalMass+=16
    if totalMass == mass:
        return True
    else:
        return False

def getMass(filename):
    """
    Gets the mass corresponding to a molecule on file.
    Takes param filename, the name of the molecule on file.
    Returns the mass corresponding to that molecule.
    """
    totalMass = 0
    if 'H' in filename:
        if filename[filename.index('H')+1].isdigit() and filename[filename.index('H')+2].isdigit():
            H = int(filename[filename.index('H')+1:filename.index('H')+2])
            totalMass+=(1*H)
        elif filename[filename.index('H')+1].isdigit():  
            H = int(filename[filename.index('H')+1])
            totalMass+=(1*H)
        else:
            totalMass+=1
    if 'N' in filename:
        if filename[filename.index('N')+1].isdigit() and filename[filename.index('N')+2].isdigit():
            N = int(filename[filename.index('N')+1:filename.index('N')+2])
            totalMass+=(14*N)
        elif filename[filename.index('N')+1].isdigit():  
            N = int(filename[filename.index('N')+1])
            totalMass+=(14*N)
        else:
            totalMass+=14
    if 'C' in filename:
        if filename[filename.index('C')+1].isdigit() and filename[filename.index('C')+2].isdigit():
            C = int(filename[filename.index('C')+1:filename.index('C')+2])
            totalMass+=(12*C)
        elif filename[filename.index('C')+1].isdigit():  
            C = int(filename[filename.index('C')+1])
            totalMass+=(12*C)
        else:
            totalMass+=12
    if 'O' in filename:
        if filename[filename.index('O')+1].isdigit() and filename[filename.index('O')+2].isdigit():
            O = int(filename[filename.index('O')+1:filename.index('O')+2])
            totalMass+=(16*O)
        elif filename[filename.index('O')+1].isdigit():  
            O = int(filename[filename.index('O')+1])
            totalMass+=(16*O)
        else:
            totalMass+=16
    return totalMass   

generateGraph = True  
while (generateGraph): #keeps running program if user wants to see more spectra
    
    os.chdir('/Users/'+username+'/Desktop') #change directory back to desktop
    os.chdir("reference_spectra")  #folder on desktop with all of the reference spectra files
    masses_on_file = []  #list to store all the molecular masses in reference spectra
    mols_on_file = []  #list to store all of the different molecules in the reference files
    spectra_files = []  #list to store the spectra for molecules with mass given by user

    for i in os.listdir(os.getcwd()):
        masses_on_file.append(getMass(i))  #adds masses to masses_on_file
    for i in os.listdir(os.getcwd()):
        mols_on_file.append(i)
    mols_on_file = mols_on_file[1:]  #gets rid of weird residual file
    
    while True:
        given_mass = raw_input("Enter the mass you would like to see the spectrum for, or enter 'c' to cancel: ")  #user enters mass
        if given_mass == 'c' or given_mass == 'C':  #user can exit program if they decide they don't want to enter any more masses
            print "\nExiting program"
            os.chdir(owd)  #change back to original directory
            sys.exit()
        elif int(given_mass) in masses_on_file:
            break
        else:
            print "No molecule found with that mass. Try again."  #asks user for mass again until mass found
    
   #gets the names of the molecules/files that match the mass given by the user   
    for i in mols_on_file:
        if isMatch(i, int(given_mass)):
            spectra_files.append(i)
            mols_on_file = mols_on_file[mols_on_file.index(i)+1:] #searches for next molecule with given mass, if applicable
    
    #if there are too many files for one mass
    overload = False
    if len(spectra_files)>2:
        overload = True
        print "\nFile overload. Here are the molecules you have to choose from: "
        print spectra_files
        selected = raw_input("\nEnter the spectra you want to see (up to 2) separated by commas: ")
        selected = list(selected.split(","))
    if overload:
        spectra_files = selected
    
    #creates dictionary for the mass and list for the intensity. to be used for plotting
    spectrum_mass = {}
    spectrum_intensity = {}
    plotMass = []
    plotIntensity = []
    
    for i in range(len(spectra_files)): 
        spectrum_mass_temp = []  #lists to store data for dictionaries
        spectrum_intensity_temp = []                                         
        with open(spectra_files[i], 'r') as f:
            numbers = []  #list to store all mass spectrum data directly from file before being processed
            for line in f:
                if line[0].isdigit():  #skips header in file
                    numbers.append(line)
            
            str_data = ''.join(numbers) #makes numbers into a string so the data can be split up
            spectrum_mass_temp.extend(int(x.split(',')[0].strip()) for x in str_data.split())  #splits up data and adds it to lists
            spectrum_intensity_temp.extend(int(x.split(',')[1].strip()) for x in str_data.split())
            spectrum_mass[spectra_files[i]] = spectrum_mass_temp  #adding the data to the dictionaries
            spectrum_intensity[spectra_files[i]] = spectrum_intensity_temp
    
    #turns the intensities into floats
    for i in spectrum_intensity:
        spectrum_intensity[i] = [(j/100.0) for j in spectrum_intensity[i]]
     
    def oldMass(mass):
        """
        Gets the floating point mass for given_mass.
        Takes param mass, the integer mass given by user.
        Returns the floating point mass.
        """   
        if float(mass)+.1 in mass_old2:
            return float(mass)+.1
        elif float(mass)+.2 in mass_old2:
            return float(mass)+.2
        elif float(mass)-.1 in mass_old2:
            return float(mass)-.1
        elif float(mass)-.2 in mass_old2:
            return float(mass)-.2
        elif float(mass)+0 in mass_old2:
            return float(mass)
    
    def oldMassMax(mass):
        """
        Gets the floating point mass for maximum mass. This is 
        so that the mass can be found in the old mass list, which 
        has most masses as floating points.
        Takes param mass, the integer mass from reference spectra.
        Returns the floating point mass.
        """
        if float(mass)+.1 in mass_old2:
            return float(mass)+.1
        elif float(mass)+.2 in mass_old2:
            return float(mass)+.2
        elif float(mass)-.1 in mass_old2:
            return float(mass)-.1
        elif float(mass)-.2 in mass_old2:
            return float(mass)-.2
        elif float(mass)+0 in mass_old2:
            return float(mass)
        elif float(mass)+1 in mass_old2:
            return float(mass)+1
        elif float(mass)+1.1 in mass_old2:
            return float(mass)+1.1
        elif float(mass)+1.2 in mass_old2:
            return float(mass)+1.2
        elif float(mass)+.9 in mass_old2:
            return float(mass)+.9
        elif float(mass)+.8 in mass_old2:
            return float(mass)+.8
    
    def oldMassMin(mass):
        """
        Gets the floating point mass for minimum mass. This is 
        so that the mass can be found in the old mass list, which 
        has most masses as floating points.
        Takes param mass, the integer mass from reference spectra.
        Returns the floating point mass.
        """
        if float(mass)+.1 in mass_old2:
            return float(mass)+.1
        elif float(mass)+.2 in mass_old2:
            return float(mass)+.2
        elif float(mass)-.1 in mass_old2:
            return float(mass)-.1
        elif float(mass)-.2 in mass_old2:
            return float(mass)-.2
        elif float(mass)+0 in mass_old2:
            return float(mass)
        elif float(mass)-1 in mass_old2:
            return float(mass)-1
        elif float(mass)-1.1 in mass_old2:
            return float(mass)-1.1
        elif float(mass)-1.2 in mass_old2:
            return float(mass)-1.2
        elif float(mass)-.9 in mass_old2:
            return float(mass)-.9
        elif float(mass)-.8 in mass_old2:
            return float(mass)-.8
        
    ###### PLOTTING ###### 
    intensities = [float(i) for i in intensities]  #makes the intensities numbers
    minMass = float(min(spectrum_mass_temp)) #gets min and max mass to align x-axis
    maxMass = float(max(spectrum_mass_temp))
    plotMass = mass_old2[mass_old2.index(oldMassMin(minMass))-5:mass_old2.index(oldMassMax(maxMass))+5]  #gets the masses and intensities for range around given mass
    plotIntensity = intensities[mass_old2.index(oldMassMin(minMass))-5:mass_old2.index(oldMassMax(maxMass))+5]
    normFactor = 99.99/(max(plotIntensity))  #normalization factor to normalize RGA intensities
    plotIntensity = [i*(normFactor) for i in plotIntensity]  #normalizes the intensities
    #remove negative intensities
    plotMass[:] = [i for i in plotMass if plotIntensity[plotMass.index(i)]>=0]
    plotIntensity[:] = [i for i in plotIntensity if i>=0]
    
    fig1 = plt.figure(1)
    if len(spectra_files)==1:  
        plt.subplot(211)  #creates subplot with 4 rows
        rowTracker = 212  #keeps track of which row to plot data on
        fig1.text(0.01, 0.63, "Relative Intensity", rotation="vertical", va="center", fontsize = 14)  #labels y axis
    elif len(spectra_files)>1 and len(spectra_files)<=2:
        plt.subplot(411)
        rowTracker = 412
        fig1.text(0.01, 0.5, "Relative Intensity", rotation="vertical", va="center", fontsize = 14)  #labels y axis
    
    pyplot.bar(plotMass, plotIntensity, width= .001, bottom = None, log = True, color = 'b', edgecolor = 'b')  #plots data
    plt.xlim(xmin= minMass-5)
    plt.xlim(xmax= maxMass+5)
    
    for i in spectra_files:
        ax1 = fig1.add_subplot(rowTracker) #creates subplots
        pyplot.bar(spectrum_mass[i], spectrum_intensity[i], width= .001, bottom = None, log = True, color = 'r', edgecolor = 'r') #adds data to plots
        plt.xlim(xmin= minMass-5)
        plt.xlim(xmax= maxMass+5)
        ax1.annotate(i[0:i.index('.')], xy=(.9,.8),xycoords='axes fraction',fontsize=13)  #labels subplots with molecule
        rowTracker+=1  #goes to next row
    
    #generates subplot that is a combination of the various reference spectra for given mass
    if len(spectra_files)>1:
        for i in spectra_files:    
            ax2 = fig1.add_subplot(rowTracker)
            pyplot.bar(spectrum_mass[i], spectrum_intensity[i], width= .001, bottom = None, log = True, color = 'm', edgecolor = 'm') #adds data to plots
            plt.xlim(xmin= minMass-5)
            plt.xlim(xmax= maxMass+5)
    
    plt.xlabel('Mass (amu)', fontsize = 14)  #labels x axis
    plt.tight_layout()  #organizes layout so there is no overlap
    
    os.chdir('/Users/'+username+'/Desktop') #change directory back to desktop
    try:
        os.mkdir('comparative_spectra')  #makes new directory on desktop to hold plots if one isn't made already
    except:
        pass
    os.chdir('comparative_spectra')
    plt.savefig(date1+ ' ' + flow + 'sccm ' + torr + ' torr ' + runNum + ' Mass-' + given_mass) #saves plot to comparative_spectra  
    plt.show() #shows plot on screen, interactive (can zoom in/out, rescale, etc.)
    
    answer = raw_input("Would you like to enter another mass (y/n)? ")  #asks if user wants to see another spectrum
    if answer == 'y' or answer == 'Y':
        generateGraph = True
        if overload:
            print "\n Previous molecules chosen: "  #displays molecules chosen so user can choose new combination
            print selected
        plt.close()  #closes plot 
    elif answer == 'n' or answer == 'N':
        generateGraph = False
        print "\nProgram over"                               
os.chdir(owd)  #change back to original directory
