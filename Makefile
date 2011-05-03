
.PHONY: all test pylint benchmark doc dochtml doclatex setup

help:
	@echo "Please use one of the following:"
	@echo "  all        Run test and doc"
	@echo "  test       Run tests and test coverage"
	@echo "  pylint     Run pylint for code quality"
	@echo "  benchmark  Performance of different variants (NOT IMPLEMENTED)"
	@echo "  doc        Generate documentation (HTML + LaTeX)"
	@echo "  dochtml    Generate documentation in HTML"
	@echo "  doclatex   Generate documentation in LaTeX"
	@echo "  setup      Try to install / update required modules"
	@echo "  distribute Perform a distribution"
	@echo "  install    Install locally"
	@echo "  clean      Remove temporary files"

all: doc test

test:
	#@coverage run rununittest.py --include="AChemKit/*"
	#@coverage report --include="AChemKit/*"
	nosetests  --with-xunit --with-coverage --cover-package=AChemKit --where=AChemKit
	#@coverage xml --include="AChemKit/*"

pylint:
	pylint --rcfile=pylint.rc -f parseable AChemKit > pylint.txt

doc: dochtml doclatex

dochtml:
	python doc/src/generate_modules.py -d doc/src/ -s rst -f -m 10 AChemKit
	sphinx-build -b html -n doc/src doc/html

doclatex:
	python doc/src/generate_modules.py -d doc/src/ -s rst -f -m 10 AChemKit
	sphinx-build -b latex -n doc/src doc/latex
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null

setup: 
	sudo apt-get install python-dev python-setuptools tofrodos
	#sudo apt-get install texlive-full #needed to build pdf docs, but big so not done by defualt
	sudo easy_install -U coverage pylint sphinx networkx

distribute: test doc
	@cp doc/src/README.rst README.txt
	@unix2dos README.txt
	@cp doc/latex/AChemKit.pdf AChemKit.pdf
	python setup.py register sdist upload

install: test
	python setup.py sdist
	sudo python setup.py install

clean:
	rm -rf *.pyc *.pyo *~
