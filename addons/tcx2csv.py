#!/usr/bin/env python

"""
File: tcx2csv.py
Author: John Letteboer (https://github.com/jletteboer/)
Date: August 25, 2016

Description:	This script is parsing Garmin Connect tcx files downloaded with the script gcexport.py from Kyle Krafka to a custom formatted csv file.

Requirements:   gcexport.py (https://github.com/kjkjava/)
"""
# Import libraries
from xml.dom import minidom
import csv
import os
import glob
import argparse

# Define header of csv file, must be the same order as row in parseTrack
header = ('actid', 'type', 'Time', 'LatitudeDegrees', 'LongitudeDegrees', 'AltitudeMeters', 'DistanceMeters', 'HeartRateBpm', 'RunCadence')

# Define Argument Parser
parser = argparse.ArgumentParser()

parser.add_argument('-f', '--format', nargs='?', choices=['tcx'], default="tcx",
    help="export format; can be only 'tcx' (default: 'tcx')")

parser.add_argument('-i', '--input', nargs='?', default=".",
    help="the directory to import to (default: '.')")

parser.add_argument('-o', '--output', nargs='?', default=".",
    help="the directory to export to (default: '.')")

args = parser.parse_args()

# Create function to parse track file.
def parseTrack(trk,actid):
    with open(args.output + actid + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for activity in trk.getElementsByTagName('Activity'):
            type = str(activity.getAttribute('Sport'))
        for trkpt in activity.getElementsByTagName('Trackpoint'):
            Time = str(trkpt.getElementsByTagName('Time')[0].firstChild.data)
            if trkpt.getElementsByTagName('LatitudeDegrees'):
                LatitudeDegrees = str(trkpt.getElementsByTagName('LatitudeDegrees')[0].firstChild.data)
                LongitudeDegrees = str(trkpt.getElementsByTagName('LongitudeDegrees')[0].firstChild.data)
            else:
                LatitudeDegrees = ''
                LongitudeDegrees = ''
            if trkpt.getElementsByTagName('AltitudeMeters'):
                AltitudeMeters = str(trkpt.getElementsByTagName('AltitudeMeters')[0].firstChild.data)
            else:
                AltitudeMeters = ''
            if trkpt.getElementsByTagName('DistanceMeters'):
                DistanceMeters = str(trkpt.getElementsByTagName('DistanceMeters')[0].firstChild.data)
            else:
                DistanceMeters = ''
            if trkpt.getElementsByTagName('RunCadence'):
                RunCadence = str(trkpt.getElementsByTagName('RunCadence')[0].firstChild.data)
            else:
                RunCadence = ''
            if trkpt.getElementsByTagName('HeartRateBpm'):
                for hr in trkpt.getElementsByTagName('HeartRateBpm'):
                    HeartRateBpm = str(hr.getElementsByTagName('Value')[0].firstChild.data)
            else:
                HeartRateBpm = ''

            row = actid, type, Time, LatitudeDegrees, LongitudeDegrees, AltitudeMeters, DistanceMeters, HeartRateBpm, RunCadence
            writer.writerow(row)

# Multiple files from directory
path = args.input + "/*.tcx"
for file in glob.glob(path):
    print(file)
    get_size = os.path.getsize(file)
    if get_size < 10000:
        print("File is to small ... skipping.....")
    else:
        actid = file.partition('_')[-1].rpartition('.')[0]
        doc = minidom.parse(file)
        doc.normalize()

        tcx = doc.documentElement

        for node in tcx.getElementsByTagName('Activities'):
            parseTrack(node, actid)
