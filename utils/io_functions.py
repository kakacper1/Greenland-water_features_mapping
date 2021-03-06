import os
import geopandas as gpd
from sentinelhub import CRS, BBox
from os import listdir
from os.path import isdir, join
from eolearn.core import EOPatch
import random


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def get_year(date_string):
    """Date input format: '2017-03-01' YYYY-MM-DD """
    return  str(date_string[:4])

def get_month(date_string):
    """Date input format: '2017-03-01' YYYY-MM-DD """
    return str(date_string[5:7])

def get_day(date_string):
    """Date input format: '2017-03-01' YYYY-MM-DD """
    return str(date_string[8:10])

def load_all_utm_zone_tiles(utm_zone, tile_size_in_km):
    """ This function loads all filed from a certain ymt zone """
    data_dir = '../../data/utm_tile_division/{1}/all_tiles_{0:.0f}x{0:.0f}km.shp'.format(tile_size_in_km, utm_zone.name )
    return gpd.read_file(data_dir)

def get_selected_tiles(gdf, top_l_x, top_l_y, bot_r_x, bot_r_y, min_idx = 0, max_idx = 100000 ):
    """ This function returns list of indexes of tiles selected by a rectangle from provided tiles """
    print('Original number of tiles:',len(gdf))
    
    selected_tiles_idxs_tmp =  gdf[gdf['index_y'].between(bot_r_y, top_l_y, inclusive=True) ]
    print('After filtering all different Y indexes:',len(selected_tiles_idxs_tmp))
    selected_tiles_idxs_second_tmp =  selected_tiles_idxs_tmp[selected_tiles_idxs_tmp['index_x'].between(top_l_x, bot_r_x, inclusive=True)]
    print('After filtering all different X indexes:',len(selected_tiles_idxs_second_tmp))
    selected_tiles_idxs_gdf =  selected_tiles_idxs_second_tmp[selected_tiles_idxs_second_tmp['index'].between(min_idx, max_idx, inclusive=True)]
    print('After filtering all different utm indexes indexes:',len(selected_tiles_idxs_gdf))
    return selected_tiles_idxs_gdf

def save_selected_tiles_to_file(selected_tiles_gdf, tile_size_in_km, site_name, crs_zone ):
    
    selected_tiles_gdf.to_crs(crs={'init': CRS.ogc_string(crs_zone)}) # world.to_crs(epsg=3395) would also work
    directory_path = '../../data/selected_tiles/'+site_name+'/'+crs_zone.name
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
    
    shapefile_filepath = directory_path+'/selected_tiles_{0:.0f}x{0:.0f}km.shp'.format(tile_size_in_km)
    selected_tiles_gdf.to_file(shapefile_filepath)
    print('File succesfully saved to:', shapefile_filepath ) 
    return

def load_selected_tiles_from_file(site_name, crs_zone, tile_size_in_km=10 ):
    """To produce a string and loads selected patches determined by site name tile size and crs zone if saved before"""
    directory_path = '../../data/selected_tiles/'+site_name+'/'+crs_zone.name
    shapefile_filepath = directory_path+'/selected_tiles_{0:.0f}x{0:.0f}km.shp'.format(tile_size_in_km)

    if os.path.isfile(shapefile_filepath):
        print ("File exists")
    else:
        print ("Requested file does not exist")
        print(shapefile_filepath)
        return 
    return gpd.read_file(shapefile_filepath)

def get_eopatches_dir(data_product='LANDSAT_8', site_name='UPE_PROMICE', crs=CRS.UTM_22N, date_range=('2013-05-01', '2013-10-31') ):
    date_range_string = '{0}_{1}-{2}_{3}'.format(get_year(date_range[0]),get_month(date_range[0]),get_year(date_range[1]),get_month(date_range[1]))
    filepath = '../../data/EOPatches/{0}/{1}/{2}/{3}/'.format(data_product,site_name,crs.name, date_range_string)
    return filepath

def get_list_of_eopatches(filepath):
    """Return list of folders names in requested directory"""
    onlyfiles = [f for f in listdir(filepath) if isdir(join(filepath, f))]
    return onlyfiles

def load_exemplary_eopatch(data_product='LANDSAT_8', date_range = ('2013-05-01', '2013-10-31'), patch_id = 5, random_choice=True ):
    eo_patch_dir = get_eopatches_dir(data_product=data_product, date_range=date_range)
    list_of_eo_patches = get_list_of_eopatches(eo_patch_dir)
    
    if list_of_eo_patches == 0:
        print('No patches found')
        return
    if random_choice == True:
        eo_patch_filename = random.choice(list_of_eo_patches)
    else:
        if patch_id < len(list_of_eo_patches):
            eo_patch_filename = list_of_eo_patches[patch_id]
        else:
            print('Index out of range')
            return
    final_eopatch_filepath = eo_patch_dir+eo_patch_filename
    print('Loaded from', final_eopatch_filepath)
    return EOPatch.load(final_eopatch_filepath)



def load_exemplary_MODIS_eopatch(data_product='MODIS', date_range = ('2013-04-26', '2013-11-05'), patch_id = 5, random_choice=True ):
    eo_patch_dir = get_eopatches_dir(data_product=data_product , date_range=date_range)
    list_of_eo_patches = get_list_of_eopatches(eo_patch_dir)
    
    if list_of_eo_patches == 0:
        print('No patches found')
        return
    if random_choice == True:
        eo_patch_filename = random.choice(list_of_eo_patches)
    else:
        if patch_id < len(list_of_eo_patches):
            eo_patch_filename = list_of_eo_patches[patch_id]
        else:
            print('Index out of range')
            return
    final_eopatch_filepath = eo_patch_dir+eo_patch_filename
    print('Loaded from', final_eopatch_filepath)
    return EOPatch.load(final_eopatch_filepath)



def load_exemplary_eopatch_from_file(file , patch_id=6, random_choice=True ):
    list_of_eo_patches = get_list_of_eopatches(file)
       
    if list_of_eo_patches == 0:
        print('No patches found')
        return
    if random_choice == True:
        eo_patch_filename = random.choice(list_of_eo_patches)
    else:
        if patch_id < len(list_of_eo_patches):
            eo_patch_filename = list_of_eo_patches[patch_id]
        else:
            print('Index out of range')
            return
    final_eopatch_filepath = file+eo_patch_filename
    print('Loaded from', final_eopatch_filepath)
    return EOPatch.load(final_eopatch_filepath)    
    