######
Readme
######

Installation
============

This package requires the following:

* Python   >= 2.5   http://www.python.org/
* Sphinx   >= 1.0   http://sphinx.pocoo.org/
* Graphviz          http://www.graphviz.org/
* Make              http://www.gnu.org/software/make/
* LaTeX             http://www.latex-project.org/
* PyLint   >=0.13.0 http://www.logilab.org/project/pylint/

For a debian-based linux distrbution, these can be installed with::

    sudo apt-get install python graphviz texlive pylint
    sudo easy_install Sphinx #only v0.6 in apt
    sudo easy_install pygments #required by sphinx
    
Optionally, the following can be installed to improve performance:

* Psyco http://psyco.sourceforge.net
* PyPy  http://codespeak.net/pypy (not implemented yet)

Currently, there is no fancy auto-installer or anything like that for this package. 

There is a makefile that will run some useful tasks for you (generate documentation, test, benchmark). This can be accessed by running the following command::

    make


Copyright
=========
This project is licensed under a modified-BSD license. See https://github.com/afaulconbridge/PyAChemKit/blob/master/COPYRIGHT
