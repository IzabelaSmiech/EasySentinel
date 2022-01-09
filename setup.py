from setuptools import setup

setup(
   name='easysentinel',
   version='0.1',
   description='here description',
   license="GPL",
   author='Izabela Smiech',
   author_email='izabelawsmiech@gmail.com',
   packages=['easysentinel'],
   install_requires=['rasterio', 'matplotlib'], #and more packages
)