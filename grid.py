import numpy as np
import itertools
import shapely.geometry as geo

def get_grid_points(southwest, northeast, lon_res, lat_res):
    min_lon = southwest[0]
    min_lat = southwest[1]
    max_lon = northeast[0]
    max_lat = northeast[1]

    N_lons = int(np.floor((max_lon - min_lon) / lon_res) + 1)
    N_lats = int(np.floor((max_lat - min_lat) / lat_res) + 1)

    latitudes = np.linspace(min_lat, max_lat, N_lats)
    longitudes = np.linspace(min_lon, max_lon, N_lons)

    return list(itertools.product(longitudes, latitudes))

def filter_points(points, shape):
    fun = lambda point: shape.contains(geo.Point(point))
    return list(filter(fun, points))
