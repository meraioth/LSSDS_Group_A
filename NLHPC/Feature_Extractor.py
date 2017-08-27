#!/bin/bash
# FATS feature extractor using OGLE lightcurves

"""
# FATS feature extractor using OGLE lightcurves

Date: 24 Aug 2017

Author: Tanveer Karim

This code is written in Python 2.7. Note that there are some bugs in the FATS package and I had to manually go into the code to fix the problems, namely include the int() function in twenty instances where I would get errors.

Here, the code will extract all the features from the lightcurves.

Update 27 Aug 2017: Updated for running in .dat files in a specified folder and produces a pandas dataframe and produces folder_output.txt file containing all the information."""


#from __future__ import division
import numpy as np
import FATS #Copy the lomb.py, FeatureFunctionLib.py and Feature.py from the github account and paste it in your username/lib/python2.7/sites-package/FATS folder

#Test timing of code. Testing 4,000 lc.
#import time

#Needed for passing arguments to Python
import sys

#To remove the FATS warnings
import warnings
warnings.filterwarnings("ignore")

#Read in folder name from terminal
folder = sys.argv[1]

# Lop over all the .dat files. Change path to the dat folder
import glob


path = folder + "/*.dat"
print(path)
resultlist = [] #For the output from FATS

#t0 = time.time() #Test time start

files = glob.glob(path)
print(files)
   
for index in xrange(len(files)):
    #Read files
    fname = files[index]
    data = np.genfromtxt(fname, usecols=(0,1,2)) #Magnitude, Time, Error in Mag

    if data.shape[0] != 0: #Some dat files are empty. This step makes sure that we are not using those.
        data = np.array([data[:,1], data[:,0], data[:,2]]) #Following the syntax from the FATS Documentation (http://isadoranun.github.io/tsfeat/FeaturesDocumentation.html)

        #FATS extracts features in this step
#        features = FATS.FeatureSpace(Data['time','magnitude','error'])
	features = FATS.FeatureSpace(featurelist=['Mean', 'Std'], Data=['time','magnitude', 'error']) #Testing two features
        result = features.calculateFeature(data)

        #This step is required to include the star ID in the dictionary
        tmp = result.result(method="dict")
        tmp['ID'] = fname[:-3] 

        resultlist.append(tmp)
        
        #Show status bar        
#        if index % 10 == 0:
#		out = index * 1. / len(files) * 100
#		sys.stdout.write("\r%d%%" % out)
#		sys.stdout.flush()

#    t1 = time.time()

#    totaltime = t1 - t0
#    print(totaltime)
    

#Convert the dictionary to pandas dataframe
import pandas as pd
dfresult = pd.DataFrame.from_dict(resultlist)

outputfilename = folder + '_output.txt'
dfresult.to_csv(outputfilename, sep=' ', index = False)

#sys.stdout.write("\r%d%%" % 100)
print("Analysis completed.")
