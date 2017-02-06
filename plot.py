#!/usr/bin/env python
# Read data from an opendap server
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

year = '2015'
month = '07'
day = '01'
curr_time = '3B42RT_Daily.%s%s%s.7.nc4' % (year, month, day)

# specify an url, the JARKUS dataset in this case
url = 'data/TRMM_RT/TRMM_3B42RT_Daily.7/%s/%s/%s' % (year, month, curr_time)
 
# create a dataset object
dataset = netCDF4.Dataset(url)
 
# Extract data from NetCDF file
lats = dataset.variables['lat'][:]  # extract/copy the data
lons = dataset.variables['lon'][:]
precipitation = dataset.variables['precipitation'][:]  # shape is lon, lat as shown above
 
# Plot of global precipitation on our random day
fig = plt.figure()
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)
# Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html
# for other projections.
m = Basemap(projection='cyl', llcrnrlat=5.0, urcrnrlat=35.0,\
            llcrnrlon=65, urcrnrlon=100, resolution='l')
#m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,\
#            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)
 
m.drawcoastlines()
m.drawmapboundary()
 
# Create 2D lat/lon arrays for Basemap
lon2d, lat2d = np.meshgrid(lons, lats)
# Transforms lat/lon into plotting coordinates for projection
x, y = m(lon2d, lat2d)
# Plot of air temperature with 11 contour intervals
cs = m.contourf(x, y, precipitation.reshape(480,1440), 11, cmap=plt.cm.Spectral_r)
cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)
 
plt.show()