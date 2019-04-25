import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd

usa = gpd.read_file('./tl_2018_us_county.shp')
print(usa.head())
print(usa.columns.values)
print(usa.STATEFP.values)
print(usa.COUNTYFP.values)
print(usa.NAME.values)
fig, ax = plt.subplots(figsize = (10,8))
print('My chemistry:', (usa.STATEFP+usa.COUNTYFP))
usa[(usa.STATEFP+usa.COUNTYFP)=='31039'].plot(ax=ax, alpha=0.3)
#plt.show()
