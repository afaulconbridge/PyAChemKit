#! /usr/bin/python
"""
Produces a `.pdf` output from a provided `.chem` format input

The output files in `.pdf` format produced using Graphviz tools.
In particular, they are constructed using :class:`AChemKit.utils.simpledot.SimpleDot`.

For information in `.chem` files see :ref:`chem_file_format`.

Usage: chem_to_pdf.py [options]

Options:

  -h, --help                     show a help message and exit
  -i INFILE, --infile=INFILE     read from INFILE (if ommited, use stdin)
  -o OUTFILE, --outfile=OUTFILE  write to OUTFILE in .pdf format  (if ommited, use stdout)
  -l LAYOUT, --layout=LAYOUT     Graphviz layout to use (if ommited, use dot)

"""

__module__="AChemKit"

#this is depcrecated in python 2.7 in favour of argparse
#however, we want python 2.5 compatibility so its still here
import optparse


from AChemKit.reactionnet import ReactionNetwork

if __name__=="__main__":

    parser = optparse.OptionParser(description="Produces `.dot` output from `.chem` input.")
    parser.add_option("-i", "--infile",  dest="infile",  help="read from INFILE (if ommited, use stdin)", metavar="INFILE")
    parser.add_option("-o", "--outfile", dest="outfile", help="write to OUTFILE in .chem format (if ommited, use stdout)", metavar="OUTFILE")
    parser.add_option("-l", "--layout", dest="layout", help="Graphviz layout to use (if ommited, use dot)", default="neato", metavar="LAYOUT")
    (options, args) = parser.parse_args()
    
    rn = None
    if options.infile is None:
        #read from standard in
        rn = ReactionNetwork.from_string(sys.stdin.read())
    else:
        #read from provided filename
        rn = ReactionNetwork.from_filename(options.infile)

    dotstr = rn.dot.plot(prog = options.layout)

    if options.outfile is None:
        #print to standard out
        sys.stdout.write(dotstr)
    else:
        #write to provided filename
        outfile = open(options.outfile, "w")
        outfile.write(dotstr)
        outfile.close()
