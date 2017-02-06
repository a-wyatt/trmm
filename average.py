#!/usr/bin/env python
import netCDF4
from scipy.stats import norm
import numpy as np
import pandas as pd
import glob

import shapefile
from shapely import geometry

def importDataset(filename):

    print('Importing...' + filename)
    # create a dataset object
    dataset = netCDF4.Dataset(filename)

    # Extract data from NetCDF file
    lats = dataset.variables['lat'][:]
    lons = dataset.variables['lon'][:]
    precipitation = dataset.variables['precipitation'][:]

    #determine shape of the arrays
    #print(lats.shape)
    #print(lons.shape)

    #import data to a dataframe, lons as index and lats as columns
    #print(pd.DataFrame(precipitation, index=lons, columns=lats).columns)

    df = pd.DataFrame(precipitation, index=lons, columns=lats)

    return df

def mid(s, offset, amount):
    return s[offset:offset+amount]

files = []

#gather all files
[files.append(f) for f in glob.iglob('data/**/*.7.nc4', recursive=True)]

#determine the unique month day combinations
timestamps = [ mid(f, 54, 8)[4:] for f in files ]

month_day = []

for i in timestamps:
  if i not in month_day:
    month_day.append(i)

#for each month and day

#Clip points within shapefile
sf = shapefile.Reader('shapefile/Country')
shapeRecs = sf.shapeRecords()

for md in month_day:
    year_files = []
    #import all files from all years for a particular month and day
    [year_files.append(yf) for yf in glob.iglob('data/**/*%s.7.nc4' % (md), recursive=True)]

    frames = [ importDataset(f) for f in year_files ]

    result = pd.concat(frames, keys=year_files)

    #DataFrame of average rainfall across timestamps
    averages = result.groupby(level=[1]).mean()

    #averages.to_csv('averages/grid/%s.csv' % (md))

    #Plot X (day) against Y (average)
    #accumulated_average_by_lat = averages.sum(axis=0)
    #accumulated_average_by_lon = averages.sum(axis=1) 

    print('Reshaping...')
    cols = averages.columns.values

    melt = pd.melt(averages.reset_index(), id_vars='index', var_name=['lat'], value_name='precipitation')
    melt.rename(columns={'index':'lon'}, inplace=True)
    #melt.to_csv('averages/reshape/%s.csv' % (md), index=False, header=True)

    points = zip(melt['lon'], melt['lat'], melt['precipitation'])

    print('Clipping...')
    for i in shapeRecs:
        shp = i.shape
        polygon = geometry.asShape(shp)
        polygon = polygon.simplify(0.2, preserve_topology=False)
        data = [(x, y, z) for x, y, z in points if geometry.Point(x, y).within(polygon)]
        pf = pd.DataFrame(data, columns=['lon', 'lat', 'precipitation'])
        pf.to_csv('averages/clipped/%s.csv' % (md), index=False, header=True)

    print('Success...')

    break

#Plotting
def plot(averages):
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
    lon2d, lat2d = np.meshgrid(averages.index.values, averages.columns.values)
    # Transforms lat/lon into plotting coordinates for projection
    x, y = m(lon2d, lat2d)
    # Plot of air temperature with 11 contour intervals
    cs = m.contourf(x, y, averages.values.reshape(480, 1440), 11, cmap=plt.cm.Spectral_r)
    cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)
     
    plt.show()

def plot_scatter(dataframe):
    fig = plt.figure()

    plt.scatter(dataframe.index, dataframe.values)

    plt.show()

#plot_scatter(accumulated_average_by_lon)
#plot(averages)