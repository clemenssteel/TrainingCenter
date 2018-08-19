'''
Created on 05.08.2018
Class to read, classify and tread separated runs from GoogleFit. Afterwards pretreated and reliable data sets are stored.
@author: Clemens Steel
'''
import os
from xml.etree.ElementTree import iterparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ghettotcx import HeartRate, LatLong, TCX

class Run:
    # Standard start of an object method
    def __init__(self, filedirectory = './example_data', filename = 'example.tcx'):
        # Object attributes are implemented by setting an standard value
        self._filedirectory = filedirectory
        self._filename = filename
        self._filepath = os.path.join(filedirectory, filename)
        # For debugging/testing purposes:
        FILEDIRECTORY = './example_data'
        FILENAME = 'example.tcx'
        FILEPATH = os.path.join(filedirectory, filename)
        self._Parser()
    def getActivity(self):
        return self._Activity

    def getDistanceMeters(self):
        return self._DistanceMeters

    def getAltitudeMeters(self):
        return self._Values

    def getAverageHeartRate(self):
        return self._AverageHearRate

    def getMaximumHeartRate(self):
        return self._MaximumHeartRate

    def getCalories(self):
        return self._Calories

    def getTotalTime(self):
        return self._TotalTime

    def getTotalTime(self):
        return self._StartTime

    def _Parser(self):
        #def _Parser(self, filedirectory = './example_data', filename = 'example.tcx'):
        "return a list of values with timestamp, heart rate given a xml file"
        #self._filedirectory = filedirectory
        #self._filename = filename
        #self._filepath = os.path.join(filedirectory, filename)
        relevant_tags = ['{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity Sport',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AverageHeartRateBpm',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumHeartRateBpm',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Notes',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}TotalTimeSeconds',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Calories',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Id'

                        ]
        group_name = ''
        counter = 0
        items = iterparse(self._filepath, events=['start'])
        Timevalue = ""
        Heartrate = ""
        self._MaximumHeartRate = ""
        self._AverageHearRate = ""
        self._Activity = ""
        self._TotalTime = ""
        self._Calories = ""
        self._DistanceMeters = ""
        AltitudeMeters = ""
        LatitudeDegrees = ""
        LongitudeDegrees = ""
        self._Values = []
        for (event, node) in items:
            counter += 1
            if node.tag not in relevant_tags:
                # Ignore anything not part of the outline
                continue
            # Output a heartrate entry
            if node.tag:
                if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Notes':
                    self._Activity = node.text.strip() if node.text else np.nan 
                    print(self._Activity)
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}TotalTimeSeconds':
                    self._TotalTime = node.text.strip() if node.text else np.nan 
                    print("Total Time "+self._TotalTime)
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Calories':
                    self._Calories = node.text.strip() if node.text else np.nan 
                    print("Calories "+self._Calories)
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Id':
                    self._StartTime = node.text.strip() if node.text else np.nan 
                    print("StartTime "+self._StartTime)
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters':
                    self._DistanceMeters = node.text.strip() if node.text else np.nan 
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees':
                    LatitudeDegrees = node.text.strip() if node.text else np.nan
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees':
                    LongitudeDegrees = node.text.strip() if node.text else np.nan 
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time':
                    Timevalue = node.text.strip() if node.text else np.nan
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters':
                    AltitudeMeters = node.text.strip() if node.text else np.nan  
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm':
                    # grab next value
                    (event, node) = next(items)
                    if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value':
                        Heartrate = node.text.strip() if node.text else np.nan
                    val = (Timevalue, Heartrate, AltitudeMeters, LatitudeDegrees, LongitudeDegrees)
                    self._Values.append(val)
                elif node.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumHeartRateBpm':
                    (event, node) = next(items)
                    if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value':
                        self._MaximumHeartRate = node.text.strip() if node.text else np.nan 
                        print("Stored MaximumHeartRate "+self._MaximumHeartRate)
                elif node.tag == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AverageHeartRateBpm':
                    (event, node) = next(items)
                    if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value':
                        self._AverageHearRate = node.text.strip() if node.text else np.nan 
                        print("Stored AverageHeartRate "+self._AverageHearRate)        
                else:
                    pass
        return self._Values
