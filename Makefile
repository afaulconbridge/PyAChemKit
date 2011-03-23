
.PHONY: doc dochtml doclatex clean test benchmark

help:
	@echo "Please use one of the following:"
	@echo "  doc        Generate documentation (HTML + LaTeX)"
	@echo "  dochtml    Generate documentation in HTML"
	@echo "  doclatex   Generate documentation in LaTeX"
	@echo "  test       Run tests and test coverage"
	@echo "  pylint     Run pylint for code quality"
	@echo "  benchmark  Run benchmarks"
	@echo "  clean      Remove all generated files"
	@echo "  all        Run clean, test, and doc"

all: clean doc

clean: 
	-rm -f test.txt
	-rm -f AChemKit.pdf
	-rm -f AChemKit/*.pyc
	-rm -f AChemKit/utils/*.pyc
	-rm -f AChemKit/tools/*.pyc
	-rm -f AChemKit/tests/*.pyc
	-rm -f AChemKit/benchmarks/*.pyc
	-rm -rf docs/AChemKit.*.rst

doc: dochtml doclatex

dochtml:
	python doc/src/generate_modules.py -d doc/src/ -s rst -f AChemKit
	sphinx-build -b html -n doc/src doc/html

doclatex:
	python doc/src/generate_modules.py -d doc/src/ -s rst -f AChemKit
	sphinx-build -b latex -n doc/src doc/latex
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null
	pdflatex -output-directory doc/latex  doc/latex/AChemKit > /dev/null
		
test:
	coverage run rununittest.py
	coverage report

pylint:
	pylint --rcfile=pylint.rc -f parseable AChemKit > pylint.txt

benchmark: 
	@echo "BENCHMAKRING NOT PROPERLY IMPLEMENTED"
