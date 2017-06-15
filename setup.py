#!/usr/bin/env python3

from distutils.core import setup

# requirements
with open('requirements.txt') as requirements:
    req = [i.strip() for i in requirements]

setup(name='pyetrade',
      version='0.1',
      description='eTrade API wrappers built on requests-oauth',
      author='Jesse Cooper',
      author_email='jesse_cooper@codeholics.com',
      url='https://github.com/jessecooper/pyetrade',
      license='GPLv3',
      packages=['pyetrade'],
      package_dir={'pyetrade':'pyetrade/'},
      install_requires = req,
      keywords = ['etrade', 'pyetrade', 'stocks']
     )
