######
Readme
######

Description
===========

PyAChemKit is a collection of Artificial Chemistry software written in Python - a library and collection of tools. 

Artificial Chemistry (AChem) is a spin-off topic of Artificial Life. AChem is aimed at emergence of life from
non-living environment - primordial soup etc.


Installation
============

To install on Ubuntu Linux, run ::

  sudo easy_install -U AChemKit

This package should work on other Linux distributions and versions of Windows, but is untested.

This package requires the following:

* Python   >= 2.6   http://www.python.org/
    
Some features use the following:

* NetworkX
* GraphViz http://www.graphviz.org/
    
Optionally, the following can be installed to improve performance:

* Psyco http://psyco.sourceforge.net
* PyPy  http://codespeak.net/pypy
        
Source
======

The latest version of the source code is available from https://github.com/afaulconbridge/PyAChemKit

The source code additionally requires the following:

* Sphinx   >= 1.0   http://sphinx.pocoo.org/
* Graphviz          http://www.graphviz.org/
* Make              http://www.gnu.org/software/make/
* LaTeX             http://www.latex-project.org/
* PyLint   >=0.13.0 http://www.logilab.org/project/pylint/
* Coverage          http://nedbatchelder.com/code/coverage/


For a Debian-based Linux distrbution --- e.g. Debian, Ubuntu --- these can be installed / updated with::

  make setup
    
(Note, LaTeX is not installed via this method because it is very large. Run ``sudo apt-get install texlive-full`` if you want to be able to compile the PDF documentation.)


There is a makefile that will run some useful tasks for you (generate documentation, test, benchmark). This can be accessed by running the following command::

    make help
    
Copyright
=========

This project is licensed under a modified-BSD license. See the fie ``COPYRIGHT`` for details.
