from distutils.core import setup

setup(name="AChemKit", \
    version="0.2.0", \
    author="Adam Faulconbridge", \
    author_email="afaulconbridge@googlemail.com", \
    packages=["AChemKit", "AChemKit/utils", "AChemKit/tools"], \
    classifiers = ["Development Status :: 3 - Alpha", \
        "Intended Audience :: Science/Research", \
        "Intended Audience :: Developers", \
        "License :: OSI Approved :: BSD License", \
        "Natural Language :: English", \
        "Operating System :: OS Independent", \
        "Programming Language :: Python", \
        "Programming Language :: Python :: 2.6", \
        "Programming Language :: Python :: 2.7", \
        "Topic :: Scientific/Engineering :: Artificial Life", \
        "Topic :: Scientific/Engineering :: Chemistry", \
        "Topic :: Software Development :: Libraries :: Python Modules"], \
    url="https://github.com/afaulconbridge/PyAChemKit", \
    download_url="http://pypi.python.org/packages/source/A/AChemKit/AChemKit-0.1.0.tar.gz#md5=a4b09ccb7ce61642305e3ef5874ac924", \
    description="An Artificial Chemistry Tookit", \
    long_description=open("README.txt").read() )
