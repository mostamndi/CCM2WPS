import numpy as np
import xarray as xr
from datetime import datetime, timedelta
from netCDF4 import date2num

#N   AEROSOL              rdrop,m
#1   'Dust accum md'      0.14E-6
#2   'Dust coarse md'     1.2E-6
#3   'Sea accum md'       0.44E-6
#4   'Sea coarse md'      2.9E-6
#5   'SO2'                1.E-6
#6   'Sulfate'            0.15E-6
#7   'BC hydrophobic'     0.02E-6
#8   'BC hydrophylic'     0.06E-6
#9   'OC hydrophobic'     0.06E-6
#10  'OC hydrophylic'     0.06E-6


data_path = "../wps"
files =["SO2", "SULF", "OH", "O3", "NO2", "MDLF", "MDBF",
        "SSLF", "SSBF", "BCHB", "BCHL", "OCHB", "OCHL", 'CH4']

fout  = "CCM_400.inst3_3d_aer_Np.1980.nc"
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

sdate=datetime(1980,1,1,0,0,0)

levs = [0.0002, 0.0003, 0.0005, 0.0007, 0.001,
          0.002, 0.003, 0.005, 0.007, 0.01,
          0.02, 0.03, 0.05, 0.07, 0.1,
          0.15, 0.2, 0.25, 0.3, 0.4,
          0.5, 0.6, 0.7, 0.85, 0.925, 1.000]


lons = np.linspace(-180, 175, 72)
lats = np.linspace(-88, 88, 45)
dates = date2num([sdate + timedelta(hours=i*6) for i in range(Ntim)], units=f"minutes since {sdate.strftime('%Y-%m-%d %H:00:00')}", calendar='gregorian')

var_3d = ["SO2", "SO4", "OH", "O3", "NO2", "DU001", "DU002",
          "SS001", "SS002","BCPHOBIC", "BCPHILIC", "OCPHOBIC", "OCPHILIC", "CH4"]

dimension = ['time', 'lev', 'lat', 'lon']
coords = {'time': dates, 'lev': levs, 'lat':lats, 'lon': lons}

attrs = [{'standard_name': 'SO2', 'long_name': 'SO2', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'SO4', 'long_name': 'SO4', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'OH', 'long_name': 'OH', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'O3', 'long_name': 'O3', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'NO2', 'long_name': 'NO2', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'DU001', 'long_name': 'DUST1', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'DU002', 'long_name': 'DUST2', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'SS001', 'long_name': 'SS001', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'SS002', 'long_name': 'SS002', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'BCPHOBIC', 'long_name': 'BCPHOBIC', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'BCPHILIC', 'long_name': 'BCPHILIC', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'OCPHOBIC', 'long_name': 'OCPHOBIC', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'OCPHILIC', 'long_name': 'OCPHILIC', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15},
         {'standard_name': 'CH4', 'long_name': 'CH4', 'units': 'kg/kg', '_FillValue':1.E+15, 'missing_value':1.E+15}
        ]
ds = {}
for i, f in enumerate(files):
    fname = f"{data_path}/{f}.STD"
    print(fname)
    data = np.fromfile(fname , dtype=np.float32).reshape([Ntim, Nlev, Nlat, Nlon])
    ds[var_3d[i]] = xr.DataArray(data=data, dims=dimension, attrs=attrs[i], coords=coords)

#dataarr2 = xr.DataArray(data2, dims=dimension, attrs=attributes2, coords=coords)
#dataset = xr.Dataset({'SO2': dataarr1, 'NO2': dataarr2})
dataset = xr.Dataset(ds)
dataset.time.attrs = {"standard_name":"time", "long_name":"time","units": f"minutes since {sdate.strftime('%Y-%m-%d %H:00:00')}", "calendar": "standard", "axis":"T"}
dataset.lon.attrs = {"standard_name":"longitude", "long_name":"longitude","units": "degrees_east", "axis":"X"}
dataset.lat.attrs = {"standard_name":"latitude", "long_name":"latitude","units": "degrees_north", "axis":"Y"}
dataset.lev.attrs = {"long_name":"vertical level", "units":"layer","axis":"Z","coordinate":"pressure", "standard_name":"pressure_layer"}
dataset.to_netcdf(fout, encoding={'time': {'dtype': 'i4'}})
print("done")






