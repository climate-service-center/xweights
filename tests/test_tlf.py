
import pytest

import xweights as xw
import xarray as xr

from . import has_dask, requires_dask
from . import has_geopandas, requires_geopandas
from . import has_intake, requires_intake
from . import has_numpy, requires_numpy
from . import has_xarray, requires_xarray
from . import has_cordex, requires_cordex
from . import has_xesmf, requires_xesmf

def test_compute_weighted_means_ds():
    netcdffile = './data/netcdf/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200701-200712.nc'

    shp = xw.get_region('states')
    ds = xr.open_dataset(netcdffile)

    assert xw.compute_weighted_means_ds(ds, shp, 
                                        time_range=['2007-01-01','2007-11-30'],
                                        subregion=['01_Schleswig-Holstein',
                                                   '02_Hamburg',
                                                   '03_Niedersachsen',
                                                   '04_Bremen'],
                                        merge_column=['all','NorthSeaCoast'],
                                        column_names=['institute_id',
                                                      'driving_model_id',
                                                      'experiment_id',
                                                      'driving_model_ensemlbe_member',
                                                      'model_id',
                                                      'rcm_version_id'])

def  test_compute_weighted_means():
    netcdffile = './data/netcdf/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200701-200712.nc'

    assert xw.compute_weighted_means(netcdffile, 'states')
