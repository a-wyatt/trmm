#basic_plot

import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

df = pd.read_csv('averages/clipped/0528.csv')

fig = plt.figure()

m = Basemap(projection='cyl', llcrnrlat=5.0, urcrnrlat=35.0,\
            llcrnrlon=65, urcrnrlon=100, resolution='l')

m.drawcoastlines()
m.drawmapboundary()

m.scatter(x=df.lon.values, y=df.lat.values, c=df.precipitation.values, s=5.0)

plt.show()