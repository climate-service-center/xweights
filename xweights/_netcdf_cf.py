from ._domains import get_domain


def adjust_vertices(ds, domain_name=None):

    def roll_vertices(bounds):
        return bounds.roll(vertices=-1)

    def correct_bounds(ds, bounds_name):
        bounds = ds.cf.get_bounds(bounds_name)
        return roll_vertices(bounds)

    def adjust_lat_lon_vertices(ds, coord_name=None, domain_name=None):

        if not ds: return
        coord = ds.cf.coordinates[coord_name]
        if len(ds[coord].dims) > 1:
            if hasattr(ds.coords[coord[0]], 'bounds'):
                return ds
                #bounds = correct_bounds(ds, 'coord_name')
                #ds_[bounds.name] = bounds
            elif hasattr(ds.coords[coord[0]], 'vertices'):
                return ds

            warnings.warn('No {} bounds found in file. Get bounds from example domain dataset.'.format(coord_name))
            if not domain_name:
                warnings.warn('No example domain is specified')
                return
            domain = get_domain(domain_name)
            bounds = correct_bounds(domain, coord_name)

            try:
                ds[bounds.name] = bounds
                ds[coord[0]].attrs['bounds'] = bounds.name
            except:
                warnings.warn('Input grid file does not match example domain dataset grid.')
                return

        return ds

    ds_c = ds.copy()

    ds_c = adjust_lat_lon_vertices(ds_c, coord_name='longitude', domain_name=domain_name)
    ds_c = adjust_lat_lon_vertices(ds_c, coord_name='latitude', domain_name=domain_name)

    return ds_c
