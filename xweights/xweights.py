from ._io import (Input,
                  adjust_name)
  
from ._regions import get_region
from ._netcdf_cf import adjust_vertices
from ._tabulator import (concat_dataframe,
                         write_to_csv)
from ._weightings import spatial_averager

import os
import warnings
import pandas as pd

def comput_weighted_means_ds(ds,
                             ds_name='dataset',
                             domain_name=None,
                             time_range=None,
                             column_names=[],
                             shp=None,
                             subregion=None,
                             merge_columns=False,
                             column_merge=False,
                             land_only=False,
                             df_output=pd.DataFrame(),
                             output=None,
                             ):

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

    column_dict = {column:ds.attrs[column] for column in column_names if hasattr(ds.attrs, column) else None}

    if os.path.isfile(shp):
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

    df_output = _concat_dataframe(df_output, variables, out, index=out.time, column_dict=column_dict, name=ds_name)

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
                           land_only=False,
                           outdir=None,
                           time_stat=False,
                           land_only=False,
                           **kwargs):

    def _calc_time_statistics(ds, statistics):
        return ds_c

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
                                              output=None,
                                              ds_name=name,
                                              )

    if outdir:
        _write_to_csv(df_output, outdir)

    return df_output

