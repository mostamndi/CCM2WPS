import numpy as np
from datetime import datetime, timedelta
from struct import pack, calcsize
import os

"""
projection	integer or string	required, must be 0, 1, 3, 4, 5
or "Equidistant_Lat_Lon", "Mercator", "Lambert", "Gaussian","Polar_Stereograhic"
date	string	required. Datetime format must be YYYY-MM-DD_hh:mm:ss
version	integer	not required, defaults to 5
forecast_hour	float	not required, defaults to 0.0
map_source	string	not required, defaults to "Unknown data source"
level	float	required
startloc	string	not required, defaults to "SWCORNER"
startlat	float	required
startlon	float	required
deltalat	float	required if projection=0; otherwise defaults to a dummy value
deltalon	float	required if projection=0 or 4; otherwise defaults to a dummy value
earth_radius	float	not required, defaults to 6367470. * 0.001
dx	float	required if projection = 1, 3, 5; otherwise defaults to a dummy value
dy	float	required if projection = 1, 3, 5; otherwise defaults to a dummy value
truelat1	float	required if projection = 1, 3, 5; otherwise defaults to a dummy value
truelat2	float	required if projection = 3; otherwise defaults to a dummy value
center_lon	float	required if projection = 3 or 5; otherwise defaults to a dummy value
nlats	float	required if projection = 4; otherwise defaults to a dummy value
is_wind_earth_relative	logical	required

   integer   :: IFV, NX, NY, IPROJ
   character :: HDATE*24, MAP_SOURCE*32, FIELD*9, UNITS*25, DESC*46
   real      :: XFCST, XLVL
   character :: startloc*8
   real      :: startlon, startlat, dx, dy, xlonc, truelat1, truelat2, nlats, earth_radius

About This Class:
This Python class is designed to convert CCM model binary data into the 
WRF Preprocessing System (WPS) Intermediate format, serving as an analog to ungrib.exe.

The class was developed as part of the LIMA Project and is intended for use 
by RSHU and LIMA members.

Details:
Developer: Suleiman Mostamandi
(Contact: suleiman@mostamandi.ru)
Version: 1.2
Date: 16 November 2024
Requirements:
Python 3 or higher
NumPy 1.26 or higher

"""


class CCM2WPS:
    CenterName = "{0:32s}".format("RSHU-CCM-MODEL")
    PREFIX = "CCM"
    header = None
    data = None
    __filename__ = ""
    __FILE__ = None

    def __init__(self, proj, iproj, Nlon, Nlat, sloc, slon, slat, dlon, dlat, eradius):
        self.proj = proj
        self.iproj = iproj
        self.Nx = Nlon
        self.Ny = Nlat
        self.dlon = dlon
        self.dlat = dlat
        self.eradius = eradius
        self.slon = slon
        self.slat = slat
        self.sloc = "{0:8s}".format(sloc)
        self.iswin = False
        return

    def setDateTime(self, newval="1980-01-01_00:00:00"):
        tmp = datetime.strptime(newval, "%Y-%m-%d_%H:%M:%S")
        self.hdate = "{0:24s}".format(newval)
        self.year = tmp.year
        self.month = tmp.month
        self.day = tmp.day
        self.hour = tmp.hour
        return

    def setFieldName(self, varname="TT", vardesc="Temperature", varunit="K"):
        self.field = "{0:9s}".format(varname)
        self.desc  = "{0:46s}".format(vardesc) 
        self.unit  = "{0:25s}".format(varunit)
        return

    def setLevel(self, lvl=200100.):
        self.level = lvl
        return

    def openFile(self, fpath=""):
        fname = f"{fpath}/{self.PREFIX}:{self.year}-{self.month:02d}-{self.day:02d}_{self.hour:02d}"
        self.__FILE__ = open(fname, "wb")
        return

    def writeFile(self):
        outfile = self.__FILE__
        # Write the format header size
        fmtstr = ">i"
        fmtsize = calcsize(fmtstr)
        outfile.write(pack(">i", fmtsize))
        outfile.write(pack(">i", 5))  # IFV
        outfile.write(pack(">i", fmtsize))

        # Write the main header
        packstr = ">24s f 32s 9s 25s 46s f 3i"
        packsize = calcsize(packstr)
        headerpack = pack(
            packstr,
            bytes(f"{self.hdate: <24}", "ascii"),  # hdate "utf-8"
            0.0,  # xfcst
            bytes(f"{self.CenterName: <32}", "ascii"),  # map_source
            bytes(f"{self.field: <9}", "ascii"),  # field
            bytes(f"{self.unit: <25}", "ascii"),  # unit
            bytes(f"{self.desc: <46}", "ascii"),  # desc
            self.level,  # xlvl
            self.Nx,  # NX
            self.Ny,  # NY
            self.iproj,  # IPROJ
        )
        outfile.write(pack(">i", packsize))
        outfile.write(headerpack)
        outfile.write(pack(">i", packsize))
        #packstr = ">8s 5f"
        packstr = ">8s 5f"
        packsize = calcsize(packstr)
        projpack = pack(
            packstr,
            bytes(f"{self.sloc: <8}", "ascii"),
            self.slat,  # START latitude
            self.slon,  # START longitude 
            self.dlat,  # DX
            self.dlon,  # DY
            self.eradius,   # Seems that I was wrong, it needs for this projection!!
        )
        outfile.write(pack(">i", packsize))
        outfile.write(projpack)
        outfile.write(pack(">i", packsize))
    
        packstr = ">i"
        packsize = calcsize(packstr)
        relpack = pack(packstr, self.iswin)
        outfile.write(pack(">i", packsize))
        outfile.write(relpack)
        outfile.write(pack(">i", packsize))
        # Array of values
        thisarr = np.asfortranarray(self.data)
        arrsize = thisarr.size
        packsize = arrsize * calcsize("f")
        outfile.write(pack(">i", packsize))
        # Write values individually using an iterator over the flattened array
        for v in thisarr.flat:
            outfile.write(pack(">f", v))
        outfile.write(pack(">i", packsize))
        return

    def closeFile(self):
        self.__FILE__.close()
        return
