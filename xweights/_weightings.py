import xesmf as xe
import xarray as xr

def spatial_averager(ds, shp):
    """xesmf's spatial averager

    Parameters
    ----------
    ds: xr.Dataset

    shp: gp.GeoDataFrame

    Returns
    -------
    out - xr.Dataset
        Dataset containing a time series of spatial averages for each geometry in ``shp``

    Example
    -------
    To create a time series of spatial averages::

        import xweights as xw
        import xarray as xr

        path = '/work/kd0956/CORDEX/data/cordex/output/EUR-11/CLMcom/MIROC-MIROC5/rcp85/r1i1p1/CLMcom-CCLM4-8-17/v1/mon/tas/v20171121/'
        netcdffile = path + 'tas_EUR-11_MIROC-MIROC5_rcp85_r1i1p1_CLMcom-CCLM4-8-17_v1_mon_200601-201012.nc'

        ds = xr.open_dataset(netcdffile)

        shp = xw.get_region('states')

        out = xw.spatial_averager(ds, shp)

    """
    savg = xe.SpatialAverager(ds, shp.geometry)
    nnz = [w.data.nnz for w in savg.weights]
    
    out = savg(ds)
    out = out.assign_coords(field_region=xr.DataArray(shp["name"], 
                                                      dims=("geom",)))
    out = out.assign_coords(nnz=xr.DataArray(nnz,
                                             dims=("geom",)))
    out = out.assign_coords(geometry=xr.DataArray(shp.geometry,
                                                  dims=("geom",)))

    return out
