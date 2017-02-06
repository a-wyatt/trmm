bash get_data.bsh

conda create -c conda-forge -n python3 python=3 anaconda netCDF4

source activate python3

conda install -c conda-forge basemap pyshp shapely

python plot.py

python average.py

worth noting .archive/ hidden folder holds grid average output zipped.