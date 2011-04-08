#! /usr/bin/python
"""
A pretty-printer and syntax checker for `.chem` files

For information in `.chem` files see :ref:`chem_file_format`.

Usage: chem_pp.py [options]

Options:

  -h, --help                     show a help message and exit
  -i INFILE, --infile=INFILE     read from INFILE (if ommited, use stdin)
  -o OUTFILE, --outfile=OUTFILE  write to OUTFILE in .chem format  (if ommited, use stdout)


"""

#this is depcrecated in python 2.7 in favour of argparse
#however, we want python 2.5 compatibility so its still here
import optparse

from AChemKit.reactionnet import ReactionNetwork

if __name__=="__main__":

    parser = optparse.OptionParser(description="Pretty-printer and syntax checker for .chem files.")
    parser.add_option("-i", "--infile",  dest="infile",  help="read from INFILE (if ommited, use stdin)", metavar="INFILE")
    parser.add_option("-o", "--outfile", dest="outfile", help="write to OUTFILE in .chem format (if ommited, use stdout)", metavar="OUTFILE")
    (options, args) = parser.parse_args()
    rn = None
    if options.infile is None:
        #read from standard in
        rn = ReactionNetwork.from_string(sys.stdin.read())
    else:
        #read from provided filename
        rn = ReactionNetwork.from_filename(options.infile)

    chemstr = str(rn)

    if options.outfile is None:
        #print to standard out
        sys.stdout.write(chemstr)
    else:
        #write to provided filename
        outfile = open(options.outfile, "w")
        outfile.write(chemstr)
        outfile.close()
