import numpy as np
from datetime import datetime, timedelta
from struct import pack, calcsize
import os, sys
from clsCCM2WPS import CCM2WPS

"""
This Python Script reads CCM Model binary files and converts into WPS intermediate format, 
using CCM2WPS Class

Details:
Developer: Suleiman Mostamandi
(Contact: suleiman@mostamandi.ru)
Version: 1.0
Date: 16 November 2024
Requirements:
Python 3 or higher
NumPy 1.26 or higher
 
"""


# Define CCM Model dimensions:
Nlon = 72    # Number of grid points along latitude
Nlat = 45    # Number of grid points along longitude
Nlev = 26    # Number of isobaric levels
Ntim = 1460  # Ntime could be defined as filesize(in bytes) / (Nlon * Nlat * Nlev * 4)

# Define CCM Model geo parameters
iproj=0          # Grid Projection ( 0 - Equidistant_Lat_Lon)
sloc='SWCORNER'  # Start position in GRID (i,j =0)
slon=-180.       # Start Longitude
slat=-88.        # Start Latitude
dlon=5.          # Spatial resolution in south - north direction
dlat=4.          # Spatial resolution in west - east direction
eradius=6367.47022 # Earth Radius, Km

levels = [0.0002, 0.0003, 0.0005, 0.0007, 0.001,
          0.002, 0.003, 0.005, 0.007, 0.01,
          0.02, 0.03, 0.05, 0.07, 0.1,
          0.15, 0.2, 0.25, 0.3, 0.4,
          0.5, 0.6, 0.7, 0.85, 0.925, 1.000]  # Looks like isobaric levels (hPa), if not, then we have to define the height of each level in meters.
# List of 3D variables:
var_3d = ["HGT", "TT", "UU", "VV", "SPECHUMD"]
# List of surface variables 2D:
var_2d = ["TT", "UU", "VV", "SPECHUMD", "LANDSEA", "PSFC", "PMSL", "SKINTEMP", "SEAICE", "SST", "SNOW", "SNOWH"]
var_2d = ["TT", "UU", "VV", "SPECHUMD", "PSFC", "PMSL", "SKINTEMP", "SNOWH"] #Some variables are not yet available
# A list of soil levels must be defined for proper conversion !!!
var_soil = ["ST000010", "ST010100",  # Soil Temperature
            "SM000010", "SM010100"]  # Soil Moisture

var_soil = ["SM000010", "SM010100"]  # Only soil moisture is availbale  

unit_3d = ["m", "K", "m s-1", "m s-1", "kg kg-1"]
unit_2d = ["K", "m s-1", "m s-1", "kg kg-1", "0/1 Flag", "Pa", "Pa", "K", "fraction", "K", "kg m-2", "m"]
unit_2d = ["K", "m s-1", "m s-1", "kg kg-1", "Pa", "Pa", "K", "m"]

unit_soil=["K", "k", "m3 m-3", "m3 m-3"]
unit_soil=["m3 m-3", "m3 m-3"]



desc_3d = ["Height", "Temperature", "U", "V", "Specific humidity"]
desc_2d = ["Temperature", "U10", "V10", "Q2", "Land/Sea flag", "Surface Pressure", "Sea-level Pressure",
           "Sea-Surface Temperature", "Sea-Ice Fraction", "Sea-Surface Temperature", "Snow Water Equivalent",
           "Physical Snow Depth"]
desc_soil = ["T of 0-10 cm ground layer", "T of 10-100 cm ground layer",
             "Soil moisture of 0-10 cm ground layer", "Soil moisture of 10-100 cm ground layer"]

desc_soil = ["Soil moisture of 0-10 cm ground layer", "Soil moisture of 10-100 cm ground layer"]


files_3d = ["HHH.STD", "TTT.STD", "UUU.STD", "VVV.STD", "QQQ.STD"]
files_2d = ["T2.STD", "U10.STD", "V10.STD", "Q2.STD", "???.STD", "PSURF.STD", "PS.STD", "TSS.STD", "???.STD", "SS.STD"]
files_2d = ["T2.STD", "U10.STD", "V10.STD", "Q2.STD", "PSURF.STD", "PS.STD", "TSS.STD", "SS.STD"]
files_soil=["???.STD", "???.STD","WS.STD", "WW.STD"]
files_soil=["WS.STD", "WW.STD"]


file_path_3d   = "/home/u004/1980_CCM/RUN_1/130/6HOUR3D"
file_path_2d   = "/home/u004/1980_CCM/RUN_1/130/6HOUR"
file_path_soil = "/home/u004/1980_CCM/RUN_1/130/6HOUR"

output_path    = "/home/u002/CCM"     # Directory where the converted files will be created.

# Now we are going to read data from binary files:
# First surface 2d variables
# Next Soil information
# Finally 3D atmospheric data

# Create New Class Instance with default parameters
ccm = CCM2WPS(proj='Equidistant_Lat_Lon',iproj=iproj, Nlon=Nlon, Nlat=Nlat, sloc=sloc,
              slon=slon, slat=slat, dlon=dlon, dlat=dlat, eradius=eradius)
# There is no information in the file about the datetime
# Here we set the start date
start_date = datetime.strptime("1980-01-01_00:00:00", "%Y-%m-%d_%H:%M:%S")
for itime in range(Ntim):
    cdate = start_date + timedelta(hours=6*itime)
    print(f"=================== Processing {cdate.strftime('%Y-%m-%d_%H:%M:%S')} ===============")
    ccm.setDateTime(cdate.strftime("%Y-%m-%d_%H:%M:%S"))
    ccm.openFile(fpath=output_path)  # Creating New CCM:YYYY-MM-DD_HH file
    # 2D Variables
    for i, v in enumerate(var_2d):
        ccm.setFieldName(varname=v, varunit=unit_2d[i], vardesc=desc_2d[i])
        v2d = np.fromfile(f"{file_path_2d}/{files_2d[i]}", dtype=np.float32,
                          offset=itime * Nlon * Nlat * 4, count=Nlon * Nlat)
        ccm.data = v2d.reshape([Nlat, Nlon])
        ccm.setLevel(lvl=201300.) if v=="PMSL" else ccm.setLevel(lvl=200100.)
        ccm.writeFile()
        print(f"2D variable ({v}) for time step {itime} added to file")
    # Soil Variables
    for j, s in enumerate(var_soil):
        ccm.setFieldName(varname=s, varunit=unit_soil[j], vardesc=desc_soil[j])
        s2d = np.fromfile(f"{file_path_soil}/{files_soil[j]}", dtype=np.float32,
                          offset=itime * Nlon * Nlat * 4, count=Nlon * Nlat)
        ccm.data = s2d.reshape([Nlat, Nlon])
        ccm.setLevel(lvl=200100.)
        ccm.writeFile()
        print(f"Soil variable ({s}) for time step {itime} added to file")
    # 3D Variables
    for k, w in enumerate(var_3d):
        ccm.setFieldName(varname=w, varunit=unit_3d[k], vardesc=desc_3d[k])
        v3d = np.fromfile(f"{file_path_3d}/{files_3d[k]}", dtype=np.float32,
                          offset=itime * Nlon * Nlat * Nlev * 4, count=Nlon * Nlat * Nlev)
        v3d = v3d.reshape([Nlev, Nlat, Nlon])
        for m, l in enumerate(levels):
            ccm.setLevel(l*100000)
            ccm.data = v3d[m]
            ccm.writeFile()
            print(f"3D variable ({w}) at level {l} for time step {itime} added to file")
    ccm.closeFile()





