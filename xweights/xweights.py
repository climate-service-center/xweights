from ._io import (Input,
                  adjust_name)
  
from ._regions import get_region
from ._netcdf_cf import adjust_vertices
from ._tabulator import (concat_dataframe,
                         write_to_csv)
from ._weightings import spatial_averager

import warnings
import pandas as pd
import geopandas as gp
import xarray as xr

def compute_weighted_means_ds(ds,
                              shp,
                              ds_name='dataset',
                              domain_name=None,
                              time_range=None,
                              column_names=[],
                              subregion=None,
                              merge_columns=False,
                              column_merge=False,
                              df_output=pd.DataFrame(),
                              output=None,
                              land_only=False,
                              time_stat=False,
                              ):

    """
    Compute spatial weighted mean of xr.Dataset

    Parameters
    ----------
    ds: xr.DataSet

    shp: str or gp.GeoDataFrame
       Name of the shapefile, pre-defined region or gp.GeoDataFrame containing the information needed for xesmf's spatial averaging

    ds_name: str (optional)
        Name of the dataset will be written to the pd.DataFrame as an extra column

    domain_name: str (optional)
        Name of the CORDEX_domain. This is only needed if ``ds`` does not have longitude and latitude vertices

    time_range: list (optional)
        List containing start and end date to select from ``ds``
        
    column_names: list (optional)
        Extra column names of the pd.DataFrame; the information is read from global attributes of ``ds``

    subregion: str or list (optional)
        Name of the subregion(s) to be selected from ``shp``

    merge_columns: str or list (optional)
        Name of the column to be merged together. Set ['all', 'newname'] to merge all geometries and set new column name to 'newname'. 

    column_merge: str (optional)
        Column name to differentiate shapefile while merging.

    ds_output: pd.DataFrame (optional)
        pd.DataFrame to be concatenated with the newly created pd.DataFrame

    output: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points\n
        !!!This is NOT implemented yet!!!\n
        As workaround write land sea mask in ``ds['mask']``. xesmf's spatial averager automatically considers ``ds['mask']``. 

    time_stat: str or list (optional)
       Do some time statistics on ``ds``\n
       !!!This is NOT implemented yet!!!

    Returns
    -------
    DataFrame : pd.DataFrame 
        pandas Dataframe containing time series of spatial averages.


    Example
    -------

    To calculate time series of spatial averages for several 'Bundeländer':\n
        - select Schleswig-Holstein, Hamburg, Bremen and Lower Saxony\n
        - Merge those regions to one new region calles NortSeaCoast\n
        - Select time slice from 2007 to 2009\n
        - Set CORDEX specific result DataFrame column names\n
    ::

        import xarray as xr
        import xweights as xw

        path = '/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/tas/v20171121/'
        netcdffile = path + 'tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc'

        ds = xr.open_dataset(netcdffile)
        df = xw.compute_weighted_means_ds(ds, 'states',
                                          subregions=['01_Schleswig-Holstein,
                                                      '02_Hamburg', 
                                                      '03_Niedersachsen', 
                                                      '04_Bremen'],
                                          merge_column=['all', 'NorthSeaCoast'],
                                          time_range=['2007-01-01','2009-12-31'],
                                          column_names=['institute_id', 
                                                        'driving_model_id', 
                                                        'experiment_id', 
                                                        'driving_model_ensemlbe_member', 
                                                        'model_id',
                                                        'rcm_version_id'],
                                          )
    """

    if land_only:
            """
            Not clear how to find right lsm file for each ds 
            Then write lsm file to ds['mask']
            The rest is done by xesmf
            """
            NotImplementedError

    ds = adjust_vertices(ds, domain_name=domain_name)

    if not isinstance(ds, xr.Dataset): return df_output

    if time_range:
        ds = ds.sel(time=slice(time_range[0], time_range[1]))

    column_dict = {column:ds.attrs[column] if hasattr(ds, column) else None for column in column_names}

    if not isinstance(shp, gp.GeoDataFrame):
        shp = get_region(shp,
                         name=subregion,
                         merge=merge_columns,
                         column=column_merge)

    out = spatial_averager(ds, shp)
    drop = [i for i in out.coords if not out[i].dims]
    out = out.drop(labels=drop)

    if time_stat:
        """
        Not sure if it is usefull to implement here or do it seperately after using xweights
        """
        NotImplementedError  

    df_output = concat_dataframe(df_output,
                                 out,
                                 column_dict=column_dict,
                                 name=ds_name)
    
    if output:
        write_to_csv(df_output, output)

    return df_output

def compute_weighted_means(input,
                           region,
                           subregion=None,
                           domain_name=None,
                           time_range=None,
                           column_names=[],
                           merge_columns=False,
                           column_merge=False,
                           outdir=None,
                           land_only=False,
                           time_stat=False,
                           **kwargs):

    """
    Compute spatial weighted mean of user-given inputs.


    Parameters
    ----------
    input: str or list
         Valid input files are netCDF file(s), directories containing those files and intake-esm catalogue files

    region: str
       Name of the shapefile or pre-defined region containing the information needed for xesmf's spatial averaging

    subregion: str or list (optional)
        Name of the subregion(s) to be selected from ``region``

    domain_name: str (optional)
        Name of the CORDEX_domain. This is only needed if ``ds`` does not have longitude and latitude vertices

    time_range: list (optional)
        List containing start and end date to be select
        
    column_names: list (optional)
        Extra column names of the pd.DataFrame; the information is read from global attributes

    merge_columns: str or list (optional)
        Name of the column to be merged together. Set ['all', 'newname'] to merge all geometries and set new column name to 'newname'.

    column_merge: str (optional)
        Column name to differentiate shapefile while merging.

    outdir: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points\n
        !!!This is NOT implemented yet!!!\n
        As workaround write land sea mask in ``ds['mask']``. xesmf's spatial averager automatically considers ``ds['mask']``. 

    time_stat: str or list (optional)
       Do some time statistics on ``ds``\n
       !!!This is NOT implemented yet!!!

    Returns
    -------
    DataFrame : pd.DataFrame 
        pandas Dataframe containing time series of spatial averages.

    Example
    -------

    To calculate time series of spatial averages for several 'Bundeländer':\n
        - select Schleswig-Holstein, Hamburg, Bremen and Lower Saxony\n
        - Merge those regions to one new region calles NortSeaCoast\n
        - Select time slice from 2007 to 2009\n
        - Set CORDEX specific result DataFrame column names\n
    ::

        import xweights as xw

        path = '/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/tas/v20171121/'
        netcdffile = path + 'tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc'

        df = xw.compute_weighted_means_ds(netcdffile, 'states',
                                          subregions=['01_Schleswig-Holstein,
                                                      '02_Hamburg', 
                                                      '03_Niedersachsen', 
                                                      '04_Bremen'],
                                          merge_column=['all', 'NorthSeaCoast'],
                                          time_range=['2007-01-01','2009-12-31'],
                                          column_names=['institute_id', 
                                                        'driving_model_id', 
                                                        'experiment_id', 
                                                        'driving_model_ensemlbe_member', 
                                                        'model_id',
                                                        'rcm_version_id'],
                                          )
    

    """

    def _calc_time_statistics(ds, statistics):
        return ds

    dataset_dict = Input(input, **kwargs).dataset_dict

    region = get_region(region, name=subregion, merge=merge_columns, column=column_merge)

    df_output = pd.DataFrame()

    for name, ds in dataset_dict.items():

        df_output = compute_weighted_means_ds(ds,
                                              domain_name=domain_name,
                                              time_range=time_range,
                                              column_names=column_names,
                                              shp=region, 
                                              subregion=subregion, 
                                              merge_columns=merge_columns, 
                                              column_merge=column_merge,
                                              land_only=land_only,
                                              df_output=df_output,
                                              ds_name=name,
                                              )

    if outdir:
        write_to_csv(df_output, outdir)

    return df_output

