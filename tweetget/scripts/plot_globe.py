#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load previously dumped DataFrame containing normalized lat/lon and plot them
"""
from __future__ import division, print_function, absolute_import

import os
import pandas as pd
from matplotlib import pyplot as plt

from twip.constant import DATA_PATH

# df = pd.io.json.json_normalize(pd.json.load(open('data.json')))
# df.to_csv('data.csv')

geo = pd.read_csv(os.path.join(DATA_PATH, 'geo_tweets.csv'), encoding='utf8', engine='python')
plt.plot(geo.lon, geo.lat, '.')
plt.xlabel('Longitude (deg)')
plt.ylabel('Latitude (deg)')
plt.show()


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
# set up orthographic map projection with
# perspective of satellite looking down at 50N, 100W.
# use low resolution coastlines.
# don't plot features that are smaller than 1000 square km.
globe = Basemap(projection='ortho', lat_0=50, lon_0=-100,
                resolution='l', area_thresh=1000.)
# draw coastlines, country boundaries, fill continents.
globe.drawcoastlines()
globe.drawcountries()
globe.fillcontinents(color='coral')
# draw the edge of the globe projection region (the projection limb)
globe.drawmapboundary()
# draw lat/lon grid lines every 30 degrees.
globe.drawmeridians(np.arange(0, 360, 30))
globe.drawparallels(np.arange(-90, 90, 30))
plt.show()


# lat/lon coordinates of five random cities from scipy example
# lats = [40.02, 32.73, 38.55, 48.25, 17.29]
# lons = [-105.16, -117.16, -77.00, -114.21, -88.10]
# cities=['Boulder, CO','San Diego, CA',
#         'Washington, DC','Whitefish, MT','Belize City, Belize']

# compute the projected coordinates for the points
x, y = globe(df.lon, df.lat)
# plot filled circles at the locations of the cities.
globe.plot(x, y,'b.')

# # plot the names of those tweets/users/etc
# for name, xpt, ypt in zip(names, x, y):
#     plt.text(xpt + 50000, ypt + 50000, name)
