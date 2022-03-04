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
        Name of the CORDEX_domain. This is only needed if `ds` does not have lon and lat vertices

    time_range: list (optional)
        List containing start and end date to select from `ds`
        
    column_names: list (optional)
        Extra column names of the pd.DataFrame; the information is read from global attributes of `ds`

    subregion: str or list (optional)
        Name of the subregion(s) to be selected from `shp`

    merge_columns: str (optional)
        Name of the column to be merged together

    column_merge: str (optional)
        Name of the new column if `merge_columns` is set

    ds_output: pd.DataFrame (optional)
        pd.DataFrame to be concatenated with the newly created pd.DataFrame

    output: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points
        !!!This is NOT implemented yet!!!
        As workaround write land sea mask in `ds`['mask']. xesmf's spatial averager automatically considers `ds`['mask'] 

    time_stat: str or list (optional)
       Do some time statistics on `ds`
       !!!This is NOT implemented yet!!!

    """

    if land_only:
            """
            Not clear how to find right lsm file for each ds 
            Then write lsm file to ds['mask']
            The rest is done by xesmf
            """
            NotImplementedError

    ds = adjust_vertices(ds, domain_name=domain_name)
    
    if not ds: return

    variables = ds.vars

    if time_range:
        ds = ds.sel(time=slice(time_range[0], time_range[1]))

    column_dict = {column:ds.attrs[column] if hasattr(ds, column) else None for column in column_names}


    if not isinstance(shp, gp.GeoDataFrame):
        shp = get_region(shp,
                         name=subregion,
                         merge=merge_columns,
                         column=column_merge)

    out = spatial_averager(ds, shp)

    if time_stat:
        """
        Not sure if it is usefull to implement here or do it seperately after using xweights
        """
        NotImplementedError  

    df_output = concat_dataframe(df_output, out, variables, index=out.time, column_dict=column_dict, name=ds_name)

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
        Name of the subregion(s) to be selected from `region`

    domain_name: str (optional)
        Name of the CORDEX_domain. This is only needed if `ds` does not have lon and lat vertices

    time_range: list (optional)
        List containing start and end date to be select
        
    column_names: list (optional)
        Extra column names of the pd.DataFrame; the information is read from global attributes

    merge_columns: str (optional)
        Name of the column to be merged together

    column_merge: str (optional)
        Name of the new column if `merge_columns` is set

    outdir: str (optional)
        Name of the output directory path or file

    land_only: bool (optional)
        Consider only land points
        !!!This is NOT implemented yet!!!
        As workaround write land sea mask in `ds`['mask']. xesmf's spatial averager automatically considers `ds`['mask'] 

    time_stat: str or list (optional)
       Do some time statistics on `ds`
       !!!This is NOT implemented yet!!!

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

