#!/usr/bin/env python3.5

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()




setup(
    name='awal',
    version='0.0.0',
    author='Aghilas Sini',
    url='https://github.com/AghilasSini/awal.git',
    description='This project is for processing under-ressourced lanuguages such as my mother language ***Kabyle*** ',
    license='Apache 2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['requests==2.8.1'],
    entry_points={
    'console_scripts':[ 'awal=awal.app:run' ],
    }
)
