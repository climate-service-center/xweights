
import pytest

import xweights as xw
import xarray as xr

from . import has_xarray, requires_xarray
from . import has_xesmf, requires_xesmf
from . import has_numpy, requires_numpy

def test_spatial_averager():
    netcdffile = './data/netcdf/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200701-200712.nc'

    shpfile = xw.get_region('states')
    ds = xr.open_dataset(netcdffile)

    assert xw.spatial_averager(ds, shp)
