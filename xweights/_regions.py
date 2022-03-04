import cordex as cx
import geopandas as gp
import pandas as pd
import os
from ._geometry import (convert_crs,
                        merge_entries)

class Regions:

    def __init__(self, geodataframe=None, selection=None):
        self.regions = ['counties', 'states', 'prudence']
        self.counties = self.Counties()
        self.states   = self.States()
        self.prudence = self.Prudence()
        self.userreg  = self.UserRegion(geodataframe, selection)

    def get_region_names(self, regionname):
        regionname   = getattr(self, regionname)
        geodataframe = regionname.geodataframe 
        regionsel    = regionname.selection
        return list(getattr(geodataframe, regionsel))

    def get_description(self, regionname):
        regionname =  getattr(self, regionname)
        return regionname.description

    def get_subset(self, regionname, subset):
        regionname   = getattr(self, regionname)
        geodataframe = regionname.geodataframe
        regionsel    = regionname.selection
        if isinstance(subset, str): subset = [subset]
        return geodataframe[geodataframe[regionsel].isin(subset)]

    class Counties:

        def __init__(self):
            self.description  = 'Counties (Landkreise) from Germany.'
            self.geodataframe =  cx.regions.germany.geodataframe('krs')
            self.selection    = 'name'

    class States:

        def __init__(self):
            self.description  = 'States (Bundesländer) from Germany'
            self.geodataframe = cx.regions.germany.geodataframe('lan')
            self.selection    = 'name'

    class Prudence:
        
        def __init__(self):
            self.description  = 'PRUDENCE regions'
            self.geodataframe = cx.regions.prudence.geodataframe
            self.selection    = 'name'     

    class UserRegion:

        def __init__(self, geodataframe, selection):
            self.description  = ''
            self.geodataframe = geodataframe
            self.selection    = selection 


def _region_dict(func, reg):
    return {name : func(name) for name in reg if hasattr(Regions, name)}

def which_regions():
    regions = Regions().regions
    func = regions.get_description
    return _region_dict(func, regions)

def which_subregions(region):
    if isinstance(region, str): region = [region]
    region = [r.lower() for r in region]
    func = Regions().get_region_names 
    return _region_dict(func, region)

def get_region(region_names, name=None, merge=None, column=None):
    gdf = []
    for region in region_names:
        if os.path.isfile(region):
            if not column:
                raise ValueError('Please set a column name.')
            geodataframe = gp.read_file(region)
            regions      = Regions(geodataframe, column)
            region       = 'userreg'
        elif hasattr(Regions(), region.lower()):
            region  = region.lower()
            regions = Regions()
            if column:
                setattr(getattr(regions, region), 'selection', column)
            else:
                column  =  getattr(regions, region).selection
        else:
            raise FileNotFoundError('File {} not available'.format(region))
        if name :
            gdf += [regions.get_subset(region, name)]
        else:
            gdf += [getattr(regions, region).geodataframe]

    gdf = gp.GeoDataFrame(pd.concat(gdf, ignore_index=True))
    gdf = convert_crs(gdf)
    if merge:
        gdf = merge_entries(gdf, merge)
    return gdf
