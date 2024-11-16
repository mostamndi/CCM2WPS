# CCM2WPS
Converts CCM model outputs to WPS Intermediate Format
About This Class:

This Python class is designed to convert CCM model binary data into the 
WRF Preprocessing System (WPS) Intermediate format, serving as an analog to ungrib.exe.

The class was developed as part of the LIMA Project and is intended for use 
by RSHU and LIMA members.

Details:
Developer: Suleiman Mostamandi
(Contact: suleiman@mostamandi.ru)
Version: 1.0
Date: 16 November 2024
Requirements:
**Python** 3 or higher
NumPy 1.26 or higher

**WPS Intermediate Format**

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

**Headers** 

   integer   :: IFV, NX, NY, IPROJ
   character :: HDATE*24, MAP_SOURCE*32, FIELD*9, UNITS*25, DESC*46
   real      :: XFCST, XLVL
   character :: startloc*8
   real      :: startlon, startlat, dx, dy, xlonc, truelat1, truelat2, nlats, earth_radius

