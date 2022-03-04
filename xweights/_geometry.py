from shapely.ops import unary_union
import geopandas as gp
import pandas as pd

def convert_crs(gdf, epsg='4326'):        
    return gdf.to_crs(epsg=epsg)

def convert_multipolygon_to_polygon(list_of_polygons):
    return unary_union(list_of_polygons)

def merge_entries(gdf, column):

    def get_polygeometry(gdf):
        list_of_polygons = [geometry for geometry in gdf.geometry]
        return [convert_multipolygon_to_polygon(list_of_polygons)]

    if isinstance(column, list): 
        column, name = column
    else:
        name = 'all'

    if column == 'all':
        dic = {'name' + [name]}
        polygeometry = get_polygeometry(gdf)
    else:
        dic = {'name' : getattr(gdf, column).unique()}
        polygeometry = []
        for values in dic.values():
            for value in values:
                polygeometry += get_polygeometry(gdf[getattr(gdf, column) == value])

    dic['geometry'] = polygeometry
    df = pd.DataFrame(dic)
    gdf = gp.GeoDataFrame(df, geometry='geometry', crs=gdf.crs)
    return gdf

