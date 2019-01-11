import os
from setuptools import setup, find_packages

version = '0.3.6'

try:
    description = file(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
except:
    description = ''

setup(name='montage',
      version=version,
      description="photogallery using decoupage",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='photo gallery decoupage',
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org/hg/montage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'decoupage >= 0.8',
        'cropresize'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [decoupage.formatters]
      images = montage.formatters:Images
      """,
      )
