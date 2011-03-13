#FOOOM!


.PHONY: doc dochtml doclatex clean test benchmark

help:
	@echo "Please use one of the following:"
	@echo "  doc        Generate documentation (HTML + LaTeX)"
	@echo "  dochtml    Generate documentation in HTML"
	@echo "  doclatex   Generate documentation in LaTeX"
	@echo "  test       Run tests" 
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
	@echo sphinx-build -b html -n docs/src docs/html

doclatex:
	@echo sphinx-build -b latex -n docs/src docs/latex
	#@echo pdflatex docs/latex
	
test: test.txt
	@echo "TESTING NOT PROPERLY IMPLEMENTED"

benchmark: 
	@echo "BENCHMAKRING NOT PROPERLY IMPLEMENTED"

test.txt: AChemKit
	-pylint --reports=n AChemKit > test.txt
	@#rpython was removed from more recent (> 03/2010) pylint versions :(
	@#-pylint --reports=n --rpython-mode -- AChemKit >> test.txt  
	python AChemKit/tests/reactionnet_test.py 2>&1 | cat >> test.txt