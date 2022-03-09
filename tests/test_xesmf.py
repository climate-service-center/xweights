
import pytest

import xweights as xw
import xarray as xr

from . import has_xarray, requires_xarray
from . import has_xesmf, requires_xesmf
from . import has_numpy, requires_numpy

def test_spatial_averager():
    netcdffile = xw.test_netcdf[0]
    shpfile = xw.get_region('states')
    ds = xr.open_dataset(netcdffile)
    assert xw.spatial_averager(ds, shp)
