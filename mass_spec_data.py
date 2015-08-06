"""  This code is to be used for mass spectrometer data analysis.
     By Sydney Riemer, June 2015 
"""

import csv
import matplotlib.pyplot as plt
from pylab import *
import numpy as numpy
import math
import sys
from matplotlib import *
from datetime import *
import time
import os
import getpass
import matplotlib.lines as mlines

programOn = True  #for determining if user wants program to be run again
while programOn:
    
    owd = os.getcwd()  #gets original working directory, sets back to this directory when code is re-run
    
    ########### BACKGROUND DATA ###########

    #ask user for the torr, run number, flow and date the data is from
    date1 = str(raw_input("Enter the date of the scan (mm-dd-yyyy): "))
    torr = str(raw_input("Enter torr: "))
    flow = str(raw_input("Enter flow: "))
    user_response = str(raw_input("Do you want to use the default background scan (y/n)? "))
    if user_response == 'y':
     filename1 = "06-02-2015 1-100 20sccm 3 torr gas scan.txt"  #default background scan
    elif user_response == 'n':
        #if background file endswith correct torr, run num, flow
            try:
                runNumB = str(raw_input("Enter run number for background: "))
            except:
                runNumB = None
            date2 = str(raw_input("Enter date for background: "))
            for i in os.listdir(os.getcwd()):
                if i.endswith(flow+"sccm "+torr+" torr gas scan "+runNumB+".txt") and i.startswith(date2):
                    filename1 = i     #gets corresponding file name       
    try:
        runNumP = str(raw_input("Enter run number for plasma: "))
    except:
        runNumP = None   #assigns no run number if no number is entered

    run_Nums1 = str(raw_input("Enter the run numbers you would like to see peak data for (or 'n' to pass this step): "))
    if run_Nums1 == 'n' or run_Nums1 == 'N':
        run_Nums_given = False
    else:
        run_Nums = run_Nums1.split(",")  #turns into a list
        run_Nums_given = True  

    #Line to start reading data from, excluding setup info at top of file
    startLine = 22
    mass = [] #list containing mass values
    intensityB = [] #list containing background intensities
    
    with open(filename1, 'rb') as background:     #opens file and reads it in
        for i in xrange(startLine):
            background.next()       #skips header at top of .txt file
        data = csv.reader(background, delimiter=',')
        for column in data:
            mass.append(column[0])   #adds masses used for background and plasma
            intensityB.append(column[1])   #adds intensities used for background
        
    ########### PLASMA DATA ###########        
        
    #searches for plasma data file corresponding to the torr entered above 
    for i in os.listdir(os.getcwd()):
        if i.endswith(flow+"sccm "+torr+" torr plasma scan "+runNumP+".txt") and i.startswith(date1):
            filename2 = i
        elif i.endswith((flow+"sccm "+torr+" torr plasma scan.txt")) and i.startswith(date1):
            filename2 =i
            
    intensityP = [] #list containing intensities
    
    try:
        with open(filename2, 'rb') as plasma:
            for i in xrange(startLine):
                plasma.next()
            data = csv.reader(plasma, delimiter=',')
            for column in data:
                intensityP.append(column[1])  #adds intensities for plasma 
    except:
        print "\nNo file found."    #if no file with that name is found
        break
            
    intensityP_ = []   #creates a new list with only intensities for masses ending in .9, .0, .1, .2
    massP = []         #only masses ending in .9, .0, .1, .2
    for i in range(len(intensityP)):
        if mass[i].endswith('.90') or mass[i].endswith('.00') or mass[i].endswith('.10') or mass[i].endswith('.20'):
            intensityP_.append(float(intensityP[i]))
            massP.append(mass[i])
    intensityP_ = [abs(i) for i in intensityP_]    #makes negative intensities in the list positive
               
    ########### PLOTTING ###########
    
    allDiffs = []   #makes new list with all of the differences, not just the ones within the error
    for i in range (0,len(mass)):
        allDiffs.append(float(intensityP[i]) - float(intensityB[i]))
    mass1 = [float(i) for i in mass]   #makes a list of masses as float values so masses vs diffs can be plotted
    
    #Graphs differences
    fig1 = plt.figure(1)
    plt.xlabel('Mass (amu)')
    plt.ylabel('Differences')
    pyplot.bar(mass1, allDiffs, width= .001, bottom = None, log = True)
    #plt.plot(mass,allDiffs, color='g') #uncomment to see the curve
        
    #Graphs background and plasma data overlapped
    fig2 = plt.figure(2)
    plt.xlabel('Mass (amu)')      #labels x and y axes
    plt.ylabel('Intensity')
    plt.plot(mass,intensityB, color='r') #background is red on graph
    plt.plot(mass,intensityP, color='b') #Plasma is blue on graph
    pyplot.yscale('log')
    #legend for graph
    red_line = mlines.Line2D([], [], color = 'red', label = 'Background')
    blue_line = mlines.Line2D([], [], color = 'blue', label = 'Plasma')
    plt.legend(handles = [blue_line, red_line])

    answer = raw_input("Would you like to set any parameters for the min/max x and y values (y/n)? ")
    if answer == "y":
        print "Enter 'd' to use default x and y values"
        xMin = raw_input("x min: ")
        xMax = raw_input("x max: ")
        yMin = raw_input("y min: ")
        yMax = raw_input("y max: ")
        if xMin == 'd':
            xMin == 0
        else: 
            plt.xlim(xmin= float(int(xMin)))
        if xMax == 'd':
            xMax == 100
        else: 
            plt.xlim(xmax= float(int(xMax)))
        if yMin == 'd':
            yMin == -.00001
        else:
            plt.ylim(ymin= float(yMin))
        if yMax == 'd':
            yMax == .00007
        else:
            plt.ylim(ymax= float(yMax))
        plt.show()
    else:
        plt.show()
    	
        ########### ANALYZE AND ORGANIZE DATA ###########
    
    ans = raw_input("Would you like to generate data tables (y/n)? ") #in case user wants a graph only
    if ans == 'n':
        print "\nGraphs generated, exiting program"
        sys.exit()
    else:
        peaks = []      #initialize a list to store the peak values
        differences = []  #initialize a list to store differences
        length = len(mass) #to use as a counter in the for loops
        error = float(raw_input("Enter error as a decimal: ")) #user enters the error they want 
    
        #only looks at data ending in .9, .0, .1, .2
        #adds differences to differences list if there is at least an x percent error between plasma and bckgrnd
        
        #1.0,1.1,1.2
        diff0 = float(intensityP[0])-float(intensityB[0])
        diff01 = float(intensityP[1])-float(intensityB[1])
        diff02 = float(intensityP[2])-float(intensityB[2])
        if float((diff0)/(float(intensityP[0]))) >= error or float(abs((diff0)/float(intensityB[0]))) >= error:
                differences.append(str(mass[0])+ ",  " +str(diff0)+",")
        if float((diff01)/(float(intensityP[1]))) >= error or float(abs((diff01)/float(intensityB[1]))) >= error:
                differences.append(str(mass[1])+ ",  " +str(diff01)+",")
        if float((diff02)/(float(intensityP[2]))) >= error or float(abs((diff02)/float(intensityB[2]))) >= error:
                differences.append(str(mass[2])+ ",  " +str(diff02)+",")
        
        #middle
        for i in range(10,length-8,10):
            diff1 = float(intensityP[i])-float(intensityB[i]) #subtract background from plasma
            diff2 = float(intensityP[i-1])-float(intensityB[i-1])
            diff3 = float(intensityP[i+1])-float(intensityB[i+1])
            diff4 = float(intensityP[i+2])-float(intensityB[i+2])
            if float((diff2)/(float(intensityP[i-1]))) >= error or float(abs((diff2)/float(intensityB[i-1]))) >= error:
                differences.append(str(mass[i-1])+ ",  " +str(diff2)+",")
            if float((diff1)/(float(intensityP[i]))) >= error or float(abs((diff1)/float(intensityB[i]))) >= error:
                differences.append(str(mass[i])+ ",  " +str(diff1)+",")
            if float((diff3)/(float(intensityP[i+1]))) >= error or float(abs((diff3)/float(intensityB[i+1]))) >= error:
                differences.append(str(mass[i+1])+ ",  " +str(diff3)+",")
            if float((diff4)/(float(intensityP[i+2]))) >= error or float(abs((diff4)/float(intensityB[i+2]))) >= error:
                differences.append(str(mass[i+2])+ ",  " +str(diff4)+",")
                
        #to account for 100 and 99.9 which get cut off in above loop
        diff5 = float(intensityP[length-1])-float(intensityB[length-1])
        diff6 = float(intensityP[length-2])-float(intensityB[length-2])
        if float((diff5)/(float(intensityP[length-1]))) >= error or float(abs((diff5)/float(intensityB[length-1]))) >= error:
            differences.append(str(mass[length-1])+ ",  " +str(diff5)+",")
        if float((diff6)/(float(intensityP[length-2]))) >= error or float(abs((diff6)/float(intensityB[length-2]))) >= error:
            differences.append(str(mass[length-2])+ ",  " +str(diff6)+",")
        
        #finds peaks in plasma data
                  
        #finds peak in first three elements: 1, 1.1, 1.2
        firstThree = [float(i) for i in intensityP[0:3]]
        massFirstThree = [mass[0:3]]
        peaks.append(str(mass[firstThree.index((max(firstThree)))]) + ",  "+ str(max(firstThree))+",")
        
        counter = 3        #counter to get mass corresponding to max intensity
        for i in range(4,len(intensityP_)-2,4):
            counter = counter
            max1 = max(intensityP_[i-1:i+3])     #gets max intensity from subsets of four (x.9,x.0,x.1,x.2)
            for j in intensityP_[i-1:i+3]:       #looks for max intensity in subsets of four
                if j!=max(intensityP_[i-1:i+3]):   #sets counter to index corresponding to max intensity, gets mass from there
                    counter+=1
                else:
                    counter=counter
                    peaks.append(massP[counter]+ ",  " + str(max1)+",")
                    counter+=1
                    
        #to account for 100 and 99.9
        if float(intensityP[length-2]) > float(intensityP[length-1]):
            peaks.append(str(mass[length-2])+ ",  " +str(float(intensityP[length-2]))+",")
        elif float(intensityP[length-2]) == float(intensityP[length-1]):
            peaks.append(str(mass[length-2])+ ",  "+str(float(intensityP[length-2]))+",")
        else:
            peaks.append(str(mass[length-1]) + ",  "+ str(float(intensityP[length-1]))+",")
        
        ######## MAKE NEW FILES AND FOLDERS ########
        
        username = getpass.getuser()  #gets username for computer   
        os.chdir('/Users/'+username+'/Desktop') #change directory to desktop
        
        #Make new folder on desktop if folder name not already taken, otherwise don't and move on
        try:
            os.mkdir('Mass spec data tables')
        except:
            pass 
            
        os.chdir('/Users/'+username+'/Desktop/Mass spec data tables') #change directory to newly made folder
        
        #Make new folder in previously made folder if folder name not already taken, otherwise don't and move on
        try:
            os.mkdir('Data tables '+ flow+'sccm '+torr+ ' torr '+runNumP) #makes new folder for each bundle of three files generated when code is run
        except:
            pass
            
        os.chdir('Data tables '+ flow+'sccm '+torr+ ' torr '+runNumP)  #change directory to new folder on desktop
        
        #saves peaks into a new file that gets saved in working directory
        name = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("/","-").replace(":","-") +" "+torr+" torr "+ str(error) + "_peak_data "+runNumP+".txt"  #file name has format date,time in military time, torr, error
        w = open(name, 'w')
        w.write("  Mass | Intensity\n")
    	for i in peaks:
            w.writelines("%s\n" % i)
        w.close()
    
        #saves differences into a new file that gets saved in working directory
        name1 = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("/","-").replace(":","-") + " "+torr+" torr "+str(error)+ "_differences_data "+runNumP+".txt"  #file name has format date,time in military time, torr, error
        writeFile = open(name1, 'w')
        writeFile.write("  Mass | Difference\n")
        for i in differences:
            writeFile.writelines("%s\n" % i)
        writeFile.close()
    
        #Read in the files created above to create final file with just mass and difference at peak
    
        peakMassTemp = [] #temporary list to store duplicates from nested for loop below
    
        #gets the masses associated with the peak values
        massPeaks = []
        with open(name, 'rb') as pf:
            data1 = csv.reader(pf, delimiter=',')
            for column in data1:
                massPeaks.append(column[0])
    
        #gets the masses associated with the differences, and gets those differences 
        massDiffs = []
        diffs = []
        with open(name1, 'rb') as df:
            for i in xrange(1):
                df.next()  
            data2 = csv.reader(df, delimiter=',')
            for column in data2:
                massDiffs.append(column[0])
                diffs.append(column[1])       
            
        #checks if a mass in the differences file has a corresponding mass in peak file
        #if it does add to peakmassTemp list
        for i in range(len(massDiffs)):
                if massDiffs[i] in massPeaks :
                    peakMassTemp.append(str(massDiffs[i]) + " " + str(diffs[i])) 
        peakMass = numpy.unique(peakMassTemp).tolist()    #new list without duplicates
    
        name2 = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("/","-").replace(":","-") + " "+torr+" torr "+str(error)+ "_peak_differences "+runNumP+".txt"
        wr = open(name2, 'w')
        wr.write("  Mass | Difference\n")
        for i in peakMass:
            wr.writelines("%s\n" % i)
        wr.close()
        
    ##### FILE WITH PEAK DIFFERENCE DATA FOR MULTIPLE PLASMA RUNS #####
    
    if run_Nums_given == True:
        multipleData = []  #new list to store the data from peak_differences files
        for i in run_Nums:
            os.chdir('/Users/'+username+'/Desktop/Mass spec data tables')  #changes directory
            os.chdir('Data tables '+ flow+'sccm '+torr+ ' torr '+i)
            for k in os.listdir(os.getcwd()):
                if k.endswith(torr+" torr "+str(error)+ "_peak_differences "+i+".txt"): #gets file name with corresponding run number
                    nameOne = k
            with open(nameOne, 'rb') as nm:
                newData = csv.reader(nm, delimiter=',')
                for j in xrange(1):
                    header = nm.next()
                multipleData.append("\nRun number " + i)
                multipleData.append(header)
                for column in newData:
                    multipleData.append(column)
    
        name3 = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace("/","-").replace(":","-") +" "+ run_Nums1 + ".txt"
        wr1 = open(name3, 'w')
        for i in multipleData:
            wr1.write(("".join(i) + "\n"))  #writes data files to new file #4 in string format
        wr1.close() 
         
    #asking user if they want to run the program again
    runAgain = raw_input("Data generated, would you like to run another set of data (y/n)? ")
    if runAgain == 'n':
        programOn = False
        os.chdir(owd)  #sets back to original working directory when code is re-run
        print "\nExiting program"
    elif runAgain == 'y':   #if yes program runs again starting at the top asking for torr and run num
        programOn == True
        os.chdir(owd)  #sets back to original working directory when code is re-run
