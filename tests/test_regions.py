
import pytest

import xweights as xw

from . import has_cordex, requires_cordex
from . import has_geopandas, requires_geopandas

def test_which_regions():
    assert xw.which_regions()

def test_which_subregions():
    assert xw.which_subregions('states')
    assert xw.which_subregions('counties')
    assert xw.which_subregions('prudence')

def test_get_region():
    assert xw.get_region('states')
    assert xw.get_region('states', name='02_Hamburg')
    assert xw.get_region('states', 
                         name=['01_Schleswig-Holstein','02_Hamburg'],
                         merge='all')
    assert xw.get_region('counties')
    assert xw.get_region('prudence')

def test_get_user_region():
    shpfile=xw.test_shp[0]
    assert xw.get_region(shpfile, merge='VA')
