#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import glob

files = glob.glob('averages/clipped/09*.csv')

#df = pd.read_csv('averages/clipped/%s.csv' % (s))
frames = [ pd.read_csv(f, index_col=['lon', 'lat']) for f in files ]
result = pd.concat(frames, keys=files)
averages = result.groupby(level=[1, 2]).mean().reset_index()

fig = plt.figure()

m = Basemap(projection='cyl', llcrnrlat=5.0, urcrnrlat=35.0,\
            llcrnrlon=65, urcrnrlon=100, resolution='l')

m.drawcoastlines()
m.drawmapboundary()

m.scatter(x=averages.lon.values, y=averages.lat.values, c=averages.precipitation.values, s=5.0)

plt.show()