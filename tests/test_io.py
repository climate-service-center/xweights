
import pytest

import xweights as xw

from . import has_intake, requires_intake
from . import has_dask, requires_dask

def test_get_dataset_dict():
    netcdffile = './data/netcdf/tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200701-200712.nc'
    
    assert xw.Input(netcdffile).dataset_dict
