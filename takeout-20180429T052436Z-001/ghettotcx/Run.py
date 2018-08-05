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

class Run:
    # Standard start of an object method
    def __init__(self, ActivitySport='Running', DistanceMeters=0, AltitudeMeters=0, AverageHeartRateBpm=0, MaximumHeartRateBpm=0, TotalTimeSeconds=0):
        # Object attributes are implemented by setting an standard value
        if ActivitySport=='Running':
            print("That is a fast run")
        elif ActivitySport=='Jogging':
            print("That is classical jogging.")
        else:
            print("That is an other sport.")
        self._ActivitySport = ActivitySport 
        self._DistanceMeters = DistanceMeters
        self._AltitudeMeters = AltitudeMeters
        self._AverageHeartRateBpm = AverageHeartRateBpm
        self._MaximumHeartRateBpm = MaximumHeartRateBpm
        def getActivitySport(self):
        return self._ActivitySport
    
        def getDistanceMeters(self):
        return self._DistanceMeters
    
        def getAltitudeMeters(self):
        return self._AltitudeMeters
    
        def getAverageHeartRateBpm(self):
        return self._AverageHearRateBpm
    
        def getMaximumHeartRateBpm(self):
        return self._MaximumHeartRateBpm
        
        def _heartrate_parser(self, filename):
        "return a list of values with timestamp, heart rate given a xml file"
        relevant_tags = ['{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm',
                         '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value',
                         
'{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity Sport',
                         
'{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters',
                         
'{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters',
                         
'{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AverageHearRateBpm',
                       
'{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumHeartRateBpm'
                        
                        ]
        group_name = ''
        counter = 0
        items = iterparse(filename, events=['start'])
        timevalue = ""
        heartrate = ""
        values = []
        for (event, node) in items:
            counter += 1
            if node.tag not in relevant_tags:
                # Ignore anything not part of the outline
                continue
            # Output a heartrate entry
            if node.tag:
                if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time':
                    timevalue = node.text.strip() if node.text else np.nan
                elif node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm':
                    # grab next value
                    (event, node) = next(items)
                    if node.tag.strip() == '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value':
                        heartrate = node.text.strip() if node.text else np.nan
                    val = (timevalue, heartrate)
                    values.append(val)
                else:
                    pass
        return values

    def ausgabe(self):
        print("Der Becher hat ein Volumen von " +str(self._Volumen)+\
              "ml und eine Füllmenge von "+str(self._Fuellmenge)+"ml.")
    def getFüllmenge(self):
        return self._Fuellmenge
    def getVolumen(self):
        return self._Volumen
    def auffüllen(self,Vein):
        Raum = self._Volumen-self._Fuellmenge
        if Raum<=Vein:
            Vein = Raum
            print("Kein Platz zum vollständigen Einfüllen!")
            self._Fuellmenge+=Vein
        else:
            self._Fuellmenge+=Vein    
        return Vein
    def entnehmen(self,Vaus):
        if self._Fuellmenge<Vaus:
            print("Es kann nicht genug entnommen werden!")
            self._Fuellmenge=0
            Entnommen = self._Fuellmenge
        else:
            Entnommen = Vaus
        return Entnommen
