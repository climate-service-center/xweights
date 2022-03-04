import xesmf as xe
import xarray as xr

def spatial_averager(ds, shp):
    savg = xe.SpatialAverager(ds, shp.geometry)
    out = savg(ds)
    out = out.assign_coords(field_region=xr.DataArray(shp["name"], 
                                                      dims=("geom",)))     
    return out
