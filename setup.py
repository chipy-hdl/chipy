from setuptools import setup, find_packages

setup(
    name='chipy',
    packages=find_packages(exclude=['tests']),
    version='0.1.1',
    description='Chipy is a single-file python module for generating digital hardware.',
    long_description=open('README.md').read(),
    author='Clifford Wolf',
    author_email='clifford@clifford.at',
    url='https://github.com/chipy-hdl/chipy',
    keywords=['eda', 'cad', 'hdl', 'verilog'],
    license='ISC'
)
