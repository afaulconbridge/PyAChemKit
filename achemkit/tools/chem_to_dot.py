#! /usr/bin/python
"""
Produces a `.dot` output from a provided `.chem` format input

The output files in `.dot` format are suitable for future processing using Graphviz tools.
In particular, they are constructed using :class:`achemkit.utils.simpledot.SimpleDot`.

For information in `.chem` files see :ref:`chem_file_format`.

Usage: chem_to_dot.py [options]

Options:

  -h, --help                     Show a help message and exit
  -i INFILE, --infile=INFILE     Read from INFILE (if ommited, use stdin)
  -o OUTFILE, --outfile=OUTFILE  Write to OUTFILE in .chem format  (if ommited, use stdout)
  -n NAMES, --names              Style of molecular species naming. One of 'full', 'id', 'blank'
  -l LAYOUT                      Layout asigned to graph

"""

import sys

#this is depcrecated in python 2.7 in favour of argparse
#however, we want python 2.5 compatibility so its still here
import optparse

from achemkit import ReactionNetwork, net_to_dot

def main():
    parser = optparse.OptionParser(description="Produces `.dot` output from `.chem` input.")
    parser.add_option("-i", "--infile",  dest="infile",  help="read from INFILE in .chem format (if ommited, use stdin)", metavar="INFILE")
    parser.add_option("-o", "--outfile", dest="outfile", help="write to OUTFILE in .dot format (if ommited, use stdout)", metavar="OUTFILE")
    parser.add_option("-n", "--names", dest="names", help="style of molecular species naming. One of 'full', 'id', 'blank'", metavar="NAMES", default=None)
    parser.add_option("-l", "--layout", dest="layout", help="layout to assign to the dot file")
    
    (options, args) = parser.parse_args()
    rn = None
    if options.infile is None:
        #read from standard in
        rn = ReactionNetwork.from_string(sys.stdin.read())
    else:
        #read from provided filename
        rn = ReactionNetwork.from_filename(options.infile)

    
    dot = net_to_dot(rn, names=options.names)
    if options.layout is not None:
        dot["graph"]["layout"] = options.layout
        
    dotstr = str(dot)

    if options.outfile is None:
        #print to standard out
        sys.stdout.write(dotstr)
    else:
        #write to provided filename
        outfile = open(options.outfile, "w")
        outfile.write(dotstr)
        outfile.close()

if __name__=="__main__":
    main()
