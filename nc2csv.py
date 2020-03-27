#!/usr/bin/python
 
# hgt to png
# Jonas Otto - helloworld@jonasotto.de
# converting NOAA Blended Sea Winds data from .nc to .csv files
# https://www.ncdc.noaa.gov/data-access/marineocean-data/blended-global/blended-sea-winds

import csv
from datetime import datetime
import argparse
import os
import sys

def convert(file_path):
    file_name = os.path.basename(file_path)
    without_extension = ".".join(file_name.split(".")[:-1])
    file_path_only = os.path.dirname(file_path)
    print_info("Starting conversion of %s." % file_name)
    start = datetime.now()
    rootgrp = Dataset(file_path, "r", format="NETCDF3")
    for key in rootgrp.variables.keys():
        print_info("key: %s, size: %d" % (key,len(rootgrp.variables[key])))
    
    for t in range(len(rootgrp.variables["time"])):
        time = rootgrp.variables["time"][t]
        csv_name = "%s_%d.csv" % (without_extension, time)
        csv_file_path = os.path.join(file_path_only, csv_name)
        with open(csv_file_path, 'w') as file:
            fnames = rootgrp.variables.keys()
            writer = csv.DictWriter(file, fieldnames=fnames)    
            writer.writeheader()
        
            print_info("writing data for t: %d" % time)
            
            for z in range(len(rootgrp.variables["zlev"])):
                zlev = rootgrp.variables["zlev"][z]
                for lat in range(len(rootgrp.variables["lat"])):
                    lattitude = rootgrp.variables["lat"][lat]
                    for lon in range(len(rootgrp.variables["lon"])):
                        longitude = rootgrp.variables["lon"][lon]
                        uVal = rootgrp.variables["u"][t][z][lat][lon]
                        vVal = rootgrp.variables["v"][t][z][lat][lon]
                        if "w" in rootgrp.variables.keys():
                            wVal = rootgrp.variables["w"][t][z][lat][lon]
                            writer.writerow({'time' : time, 'zlev': zlev, 'lat': lattitude, 'lon': longitude, 'u': uVal, 'v': vVal, 'w': wVal})
                        else:
                            writer.writerow({'time' : time, 'zlev': zlev, 'lat': lattitude, 'lon': longitude, 'u': uVal, 'v': vVal})
        
    rootgrp.close()
    end = datetime.now()
    duration = end - start
    mins = duration.total_seconds() / 60.0
    print_info("Finised converting %s" % file_name)
    print_info("Processing time: %f minutes" % mins)
    print_line()

def get_ncfiles_from_folder(folder_path):
    files = os.listdir(folder_path)
    ncfiles = [os.path.join(folder_path,file) for file in files if file.endswith(".nc")]
    return ncfiles

def main():
    start = datetime.now()
    
    parser = argparse.ArgumentParser(description='Converting NOAA Blended Sea Winds data from .nc to .csv files')
    parser.add_argument('--file', help='A single .nc file to convert')
    parser.add_argument('--folder', help='A folder of files to batch convert')

    args = parser.parse_args()

    ncFile = args.file
    ncFolder = args.folder

    files_to_convert = []

    if ncFolder is None and ncFile is not None:
        # single file conversion
        print_info("Attempting a single file conversion")
        files_to_convert.append(ncFile)
    elif ncFile is None and ncFolder is not None:
        # batch conversion
        print_info("Attempting a batch file conversion")
        files_to_convert = get_ncfiles_from_folder(ncFolder)
    elif ncFile is None and ncFolder is None:
        # you retard did it wrong
        print_warning("Please supply a file or a folder.")
        print_warning("Run python nc2csv.py --help for more information.")
        exit()
    else:
         # you retard did it wrong
        print_warning("Please only supply a file OR a folder. Not both.")
        print_warning("Run python nc2csv.py --help for more information.")
        exit()
    
    print_info("Found %d .nc files to convert." % (len(files_to_convert)) )
    
    for i,file in enumerate(files_to_convert):
        print_info("%i / %i" % (i, len(files_to_convert)))
        convert(file)
    end = datetime.now()
    duration = end - start
    mins = duration.total_seconds() / 60.0
    print_info("Finished converting all .nc files to .csv files.")
    print_info("Processing time: %f minutes" % mins)
    print_info("You can find all generated .csv files in %s" % os.path.basename(files_to_convert[0]))

def print_line():
    print("----------------------------------------------------------------------------------")

def print_info(info_text):
    #prints in green
    print('\033[92m' + info_text + '\033[0m')

def print_warning(warning_text):
    #prints in red
    print('\033[91m' + warning_text + '\033[0m')

#os.system('color')
print_line()
try:
    from netCDF4 import Dataset
except ImportError as error:
    print_warning("Error: Couldn't import the netCDF4 library.")
    print_warning("Please install via pip install -r requirements.txt or pip install netCDF4.")
    print_line()
    exit()

if __name__ == "__main__":
   main()