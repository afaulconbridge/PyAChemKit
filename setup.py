from setuptools import setup, find_packages

import achemkit

setup(name="AChemKit", 
    version=achemkit.__version__, 
    author="Adam Faulconbridge", 
    author_email="afaulconbridge@googlemail.com", 
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha", 
        "Intended Audience :: Science/Research", 
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: BSD License", 
        "Natural Language :: English", 
        "Operating System :: OS Independent", 
        "Programming Language :: Python", 
        "Programming Language :: Python :: 2.6", 
        "Programming Language :: Python :: 2.7", 
        "Topic :: Scientific/Engineering :: Artificial Life", 
        "Topic :: Scientific/Engineering :: Chemistry", 
        "Topic :: Software Development :: Libraries :: Python Modules"], 
    url="https://github.com/afaulconbridge/PyAChemKit", 
    description="An Artificial Chemistry Tookit", 
    long_description=open("README.txt").read(),
    entry_points = {
        'console_scripts': ['chem_pp = achemkit.tools.chem_pp:main', 
        'chem_to_dot = achemkit.tools.chem_to_dot:main',
        'chem_to_pdf = achemkit.tools.chem_to_pdf:main',
        ]},
    install_requires = [
        'networkx',
        'pyumpf'    
    ]
    )
