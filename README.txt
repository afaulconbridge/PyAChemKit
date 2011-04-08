######
Readme
######

Description
===========

PyAChemKit is a Python implementation of an Artificial Chemistry Kit - a library and collection of tools. 

Artificial Chemsistry (AChem) is a spin-off topic of Artificial Life. AChem is aimed at emergence of life from
non-living environment - primordial soup etc.


Installation
============

To install on Unix/Linux, run ::

sudo python setup.py install

This package should work on windows, but is untested.

This package requires the following:

* Python   >= 2.6   http://www.python.org/
    
Optionally, the following can be installed to improve performance:

* Psyco http://psyco.sourceforge.net
* PyPy  http://codespeak.net/pypy
        
Source
======

Source code is available from https://github.com/afaulconbridge/PyAChemKit

The source code additionally requires the following:

* Sphinx   >= 1.0   http://sphinx.pocoo.org/
* Graphviz          http://www.graphviz.org/
* Make              http://www.gnu.org/software/make/
* LaTeX             http://www.latex-project.org/
* PyLint   >=0.13.0 http://www.logilab.org/project/pylint/
* Coverage          http://nedbatchelder.com/code/coverage/


For a debian-based linux distrbution, these can be installed with::

    sudo apt-get install python graphviz texlive
    sudo easy_install Sphinx #only v0.6 in apt
    sudo easy_install pygments #required by sphinx


There is a makefile that will run some useful tasks for you (generate documentation, test, benchmark). This can be accessed by running the following command::

    make help
    
Copyright
=========

This project is licensed under a modified-BSD license. See COPYRIGHT file for details.
