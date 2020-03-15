import matplotlib.pyplot as plt
from sentinelhub import CRS, BBox
import os
import numpy as np
import geopandas as gpd
from scipy import ndimage

def plot_matrix(eopatch_dem):
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(eopatch_dem.squeeze())
    plt.xticks([])
    plt.yticks([])
    return

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


def plot_RGB_LANDSAT_8_image(eopatch, data_acces_name='LANDSAT_RAW_BANDS' ,datetime_idx=0, red_id=4, green_id=3, blue_id=2, save=False, plot_folder='plots'):
    print(eopatch.timestamp[datetime_idx])
    print('Ploting...')
    fig = plt.figure(figsize=(20, 20))
    plt.imshow(np.clip(eopatch.data[data_acces_name][datetime_idx][..., [red_id, green_id, blue_id]] * 3.5, 0, 1))
    if save:
        image_name ='{0}_{1}_{2}_{3}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],datetime_idx,data_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', image_name )
    del eopatch
    return

def plot_single_band_LANDSAT_8(eopatch, data_acces_name='LANDSAT_RAW_BANDS', band_idx=0, datetime_idx=0, save=False, plot_folder='plots'):
    print(eopatch.timestamp[datetime_idx])
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(eopatch.data[data_acces_name][datetime_idx][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    if save:
        image_name ='{0}_{1}_{2}_{3}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],datetime_idx,data_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', image_name )
    del eopatch
    return

def plot_single_mask_LANDSAT_8(eopatch, data_acces_name='LANDSAT_RAW_BANDS', band_idx=0, datetime_idx=0, save=False, plot_folder='plots'):
    print(eopatch.timestamp[datetime_idx])
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(eopatch.mask[data_acces_name][datetime_idx][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    if save:
        image_name ='{0}_{1}_{2}_{3}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],datetime_idx,data_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', image_name )
    del eopatch
    return

#def plot_qa_mask_LANDSAT_8(eopatch, band_idx, mask_acces_name='LANDSAT_QA_LAYERS', datetime_idx =0, dilation=0 ):
#    fig = plt.figure(figsize=(10, 10)) 
#    print(eopatch.timestamp[datetime_idx])
#    
#    if dilation != 0:
#        dilated_mask = ndimage.binary_dilation(eopatch.data[mask_acces_name][datetime_idx][..., band_idx].squeeze(), iterations=dilation) 
#    print('Mask dilated: ', dilation, 'times.')
#    
#    dilated_mask()
#    plt.imshow()
#    plt.xticks([])
#    plt.yticks([])
#    del eopatch
#    return


def plot_timeless_mask_LANDSAT_8(eopatch, band_idx, mask_acces_name='DEM_RAW_LAYER', save=False, plot_folder='plots' ):
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(eopatch.mask_timeless[mask_acces_name][..., band_idx].squeeze())
    plt.xticks([])
    plt.yticks([])
    if save:
        image_name ='{0}_{1}_{2}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],mask_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', plot_folder+image_name )
    del eopatch
    return

def plot_timeless_mask_LANDSAT_8_max_min_val(eopatch, band_idx, mask_acces_name='DEM_RAW_LAYER', save=False, plot_folder='plots', cmap=plt.cm.viridis ):
    vmin, vmax = None, None
    data = eopatch.mask_timeless[mask_acces_name][..., band_idx].squeeze()
    vmin = np.min(data) if vmin is None else (np.min(data) if np.min(data) < vmin else vmin)
    vmax = np.max(data) if vmax is None else (np.max(data) if np.max(data) > vmax else vmax)
    fig = plt.figure(figsize=(10, 10)) 
    plt.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap)
    if save:
        image_name ='{0}_{1}_{2}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],mask_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', plot_folder+image_name )
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

def plot_qa_mask_LANDSAT_8(eopatch, band_idx, mask_acces_name='LANDSAT_QA_LAYERS', datetime_idx =0, dilation=0 ):
    fig = plt.figure(figsize=(10, 10)) 
    print(eopatch.timestamp[datetime_idx])
    binary_mask = eopatch.data[mask_acces_name][datetime_idx][..., band_idx].squeeze().round().astype(bool)
    if dilation != 0:
        binary_mask = ndimage.binary_dilation(binary_mask, iterations=dilation) 
        print('Mask dilated: ', dilation, 'times.')
    
    plt.imshow(binary_mask)
    plt.xticks([])
    plt.yticks([])
    del eopatch
    return

def plot_RGB_MODIS_image(eopatch, data_acces_name='MODIS_RAW_BANDS' ,datetime_idx=0, red_id=0, green_id=3, blue_id=2, save=False, plot_folder='plots'):
    print(eopatch.timestamp[datetime_idx])
    print('Ploting...')
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(np.clip(eopatch.data[data_acces_name][datetime_idx][..., [red_id, green_id, blue_id]], 0, 1))
    if save:
        image_name ='{0}_{1}_{2}_{3}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],datetime_idx,data_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', image_name )
    del eopatch
    return

def plot_all_bands_in_data_acces_name(eopatch, data_acces_name='LANDSAT_RAW_BANDS', datetime_idx=0, save=False, plot_folder='plots'):
    print(eopatch.timestamp[datetime_idx])
    
    data_one_day = eopatch.data[data_acces_name][datetime_idx]#
    total_bands_no = data_one_day.shape[2]
    
    for band_idx in range(total_bands_no):
        fig = plt.figure(figsize=(10, 10)) 
        print('Band:', band_idx )
        data_single_band = data_one_day[..., band_idx].squeeze()
        plt.imshow(data_single_band)
        
    if save:
        image_name ='{0}_{1}_{2}_{3}.png'.format(eopatch.meta_info['patch_index'], eopatch.meta_info['time_interval'][0][:4],datetime_idx,data_acces_name)
        plt.savefig(plot_folder+image_name)
        print('Saved:', image_name )
    del eopatch
    return
