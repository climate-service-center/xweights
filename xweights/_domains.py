import cordex as cx

class Domains:

    def __init__(self):
        self.domains = cx.core.domain.domain_names()

domains = Domains()

def which_domains(name=None):
    return domains.domains

def get_domain(domain):
    return cx.cordex_domain(domain, add_vertices=True)

def crop_to_domain(ds, domain):
    domain = get_domain(domain)
    return ds.sel(
        rlon=slice(domain.rlon.min(), domain.rlon.max()),
        rlat=slice(domain.rlat.min(), domain.rlat.max()),
    )

