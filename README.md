# Info
A small python3 script converting NOAA Blended Sea Winds data from .nc to .csv files.
See https://www.ncdc.noaa.gov/data-access/marineocean-data/blended-global/blended-sea-winds

The conversion process is really sloooow and creates huge files. Hit me up if you have an idea on how to make it faster.

# Install
> pip install -r requirements.txt

# Usage:
Single file convert:
> python nc2csv.py --file <inputfile.nc>

Batch convert all files in the supplied folder:
> python nc2csv.py --folder </path/to/folder>

Help:
> python nc2csv.py --help