# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyCuT',
    version='0.0.1',
    description='Text-based user interfaces framework and widget toolkit for creating classic and embedded graphical user interfaces',
    long_description=readme,
    author='Eugenio Parodi',
    author_email='ceccopierangiolieugenio@googlemail.com',
    url='https://github.com/ceccopierangiolieugenio/pyCuT',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
