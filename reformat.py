#!/usr/bin/env python
import netCDF4
from scipy.stats import norm
import numpy as np
import pandas as pd
import glob

import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

df = pd.read_csv('averages/0101.csv', index_col=0)

cols = df.columns.values

print(cols)
upvt = pd.melt(df, id_vars=df.index.values, value_vars=[cols])

print(upvt.head(10))


