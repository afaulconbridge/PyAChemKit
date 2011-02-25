#! /usr/bin/python
"""
Produces a `.dot` output from a provided `.chem` format input

The output files in `.dot` format are suitable for future processing using Graphviz tools.
In particular, they are constructed using :class:`AChemKit.utils.simpledot.SimpleDot`.

For information in `.chem` files see :ref:`chem_file_format`.

Usage: chem_to_dot.py [options]

Options:

  -h, --help                     Show a help message and exit
  -i INFILE, --infile=INFILE     Read from INFILE (if ommited, use stdin)
  -o OUTFILE, --outfile=OUTFILE  Write to OUTFILE in .chem format  (if ommited, use stdout)
  -n NAMES, --names              Style of molecular species naming. One of 'full', 'id', 'blank'

"""

__module__ = "AChemKit.tools"

import sys
#this will not be required once a proper installer exists
sys.path.append("..")

#this is depcrecated in python 2.7 in favour of argparse
#however, we want python 2.5 compatibility so its still here
import optparse

#temporarilly mangle the path to access it properly
import sys
sys.path.append("/home/adam/Dropbox/AChemKit")

from AChemKit.bucket import Bucket

if __name__=="__main__":

    parser = optparse.OptionParser(description="Produces `.dot` output from `.chem` input.")
    parser.add_option("-i", "--infile",  action="store", type="string", dest="infile",  help="read from INFILE in .log format (if ommited, use stdin)", metavar="INFILE")
    parser.add_option("-o", "--outfile", action="store", type="string", dest="outfile", help="write to OUTFILE in .chem format (if ommited, use stdout)", metavar="OUTFILE")
    parser.add_option("-a", "--after", action="store", type="float", dest="after", help="only use events after this time", default=0.0)
    (options, args) = parser.parse_args()
    rn = None
    if options.infile is None:
        #read from standard in
        b = Bucket.from_string(sys.stdin.read())
    else:
        #read from provided filename
        b = Bucket.from_filename(options.infile)

    newevents = filter(lambda x: x.time > options.after, b.events)
    nb = Bucket(newevents)
    chemstr = str(nb.reactionnet)

    if options.outfile is None:
        #print to standard out
        sys.stdout.write(chemstr)
    else:
        #write to provided filename
        outfile = open(options.outfile, "w")
        outfile.write(chemstr)
        outfile.close()


