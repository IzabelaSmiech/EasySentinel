from setuptools import setup

setup(
   name='easysentinel',
   version='0.1',
   description='Some simple stuff regarding work with raster imagery from Sentinel-2 mission. Enjoy exploring!',
   license="GPL",
   author='Izabela Smiech',
   author_email='izabelawsmiech@gmail.com',
   packages=['easysentinel'],
   install_requires=['rasterio', 'matplotlib', 'seaborn', 'shapely', 'fiona', 'random', 'numpy']
)