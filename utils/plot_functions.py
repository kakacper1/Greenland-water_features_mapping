import matplotlib.pyplot as plt
from sentinelhub import CRS, BBox
import os
import numpy as np
import geopandas as gpd

def display_greenland_with_tiles(gdf, crs_zone, display_indexes=False):
    """Display greeenland borders with selected tiles with indexes"""
    
    # Folder where Greenland outline data is stored:
    DATA_FOLDER = os.path.join('..', '..', 'data', 'geoJSONs')
    # import geojson of Greenland:
    grl_geo_json = gpd.read_file(os.path.join(DATA_FOLDER, 'GRL.geojson'))
    print('Succesfully loaded Greenland contour. Current CRS:', grl_geo_json.crs)
    # change CRS
    grl_geo_json_UTM_zone = grl_geo_json.to_crs(crs={'init': CRS.ogc_string(crs_zone)})
    # Check what crs is obtained outline now:
    print('CRS chnaged:', grl_geo_json_UTM_zone.crs)
    
    # DISPLAY RESULTS:
    # set up font
    fontdict = {'family': 'monospace', 'weight': 'normal', 'size': 8}
    if display_indexes:
        # if bboxes have all same size, estimate offset
        xl, yl, xu, yu = gdf.iloc[0].geometry.bounds
        xoff, yoff = (xu-xl)/3, (yu-yl)/5
    
    #figure 
    fig, ax = plt.subplots(figsize=(200, 360))
    gdf.plot(ax=ax,facecolor='w',edgecolor='r',alpha=0.5)
    grl_geo_json_UTM_zone.plot(ax=ax, facecolor='w',edgecolor='b',alpha=0.5, linewidth=4)
    plt.title(crs_zone.name + 'zone of Greenland')
    plt.axis('on')
    if display_indexes:
        for idx in gdf.index:
            eop_name = '{0}x{1}'.format(gdf.index_x[idx], gdf.index_y[idx])
            centroid, = list(gdf.geometry[idx].centroid.coords)
            ax.text(centroid[0]-xoff, centroid[1]+yoff, '{}'.format(idx), fontdict=fontdict)
            ax.text(centroid[0]-xoff, centroid[1]-yoff, eop_name, fontdict=fontdict)
    
    return


def plot_RGB_LANDSAT_8_image(eopatch, data_acces_name='LANDSAT_RAW_BANDS' ,datetime_idx=0, red_id=4, green_id=3, blue_id=2  ):
    
    fig = plt.figure(figsize=(20, 20))

    print(eopatch.timestamp[datetime_idx])
    plt.imshow(np.clip(eopatch.data[data_acces_name][datetime_idx][..., [red_id, green_id, blue_id]] * 3.5, 0, 1))
    plt.xticks([])
    plt.yticks([])
    del eopatch
    return

def plot_single_band_LANDSAT_8(eopatch, band_idx, data_acces_name='LANDSAT_RAW_BANDS' ,datetime_idx =0 ):
    fig = plt.figure(figsize=(10, 10)) 
    print(eopatch.timestamp[datetime_idx])
    plt.imshow(eopatch.data[data_acces_name][datetime_idx][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    del eopatch
    return

def plot_qa_mask_LANDSAT_8(eopatch, band_idx, mask_acces_name='LANDSAT_QA_LAYERS', datetime_idx =0 ):
    fig = plt.figure(figsize=(10, 10)) 
    print(eopatch.timestamp[datetime_idx])
    plt.imshow(eopatch.data[mask_acces_name][datetime_idx][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    del eopatch
    return


def plot_timeless_mask_LANDSAT_8(eopatch, band_idx, mask_acces_name='DEM_RAW_LAYER' ):
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(eopatch.data_timeless[mask_acces_name][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    del eopatch
    return

def plot_RGB_MODIS_image(eo_patch, data_acces_name, datetime_idx, red_idx=0 , green_idx=3, blue_idx=2  ):
    """Display MODIS RGB picture accordingly to the specified date and band indexes"""
    fig = plt.figure(figsize=(10, 10))
    print(eo_patch.timestamp[datetime_idx])
    plt.imshow(eo_patch.data[data_acces_name][datetime_idx][..., [red_idx, green_idx, blue_idx]].squeeze())
    plt.xticks([])
    plt.yticks([])
    return