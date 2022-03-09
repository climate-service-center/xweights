from pathlib import Path

data_path = Path(__file__).parent 

netcdf = list((data_path / "data/netcdf").glob('*'))

shp = list((data_path / "data/shp").glob('*.shp'))
