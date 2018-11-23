#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys

with io.open('./rpkflashtool/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

install_requires = [
    'esptool==2.5.1',
    'PyQt5==5.11.2',
    'pyserial==3.4',
    'appdirs==1.4.3'
]

setup(
    name='rpkflashtool',
    version=version,
    description='A simple Flasher for Kano Pixel Kit.',
    long_description='Flash your Pixel Kit with MicroPython or Kano Code firmware.',
    author='Murilo Polese',
    author_email='murilopolese@gmail.com',
    url='https://github.com/murilopolese/kano-pixel-kit-flash-tool',
    license='MIT license',
    packages=['rpkflashtool'],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    classifiers=[]
)
