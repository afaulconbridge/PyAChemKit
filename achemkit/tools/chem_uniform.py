"""

This is a command-line tool for generating `.chem` files using the :py:func:`~AChemKit.randomnet.Uniform` random reaction network algorithm.

"""

import random
import argparse

import AChemKit
from AChemKit.randomnet import Uniform 

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Generates `.chem` using Uniform algorithm.")
    parser.add_argument("-o", "--outfile", action="store", type=argparse.FileType('w'), help="write to OUTFILE in .chem format (if ommited, use stdout)", metavar="OUTFILE")
    parser.add_argument("-n", "--nmols", action="store", type=int, help="number of molecules", default=10)
    parser.add_argument("-m", "--nreactions", action="store", type=int, help="number of reactions", default=10)
    parser.add_argument("-r", "--nreactants", action="append", help="possible number of reactants", default=[2])
    parser.add_argument("-p", "--nproducts", action="append", help="possible number of products", default=[2])
    parser.add_argument("-t", "--rates", action="append", help="possible reaction rates", default=[1.0])
    parser.add_argument("-s", "--seed", action="store", type=int, help="pseudo-random seed", default=None)
    args = parser.parse_args()
    
    nmols = args.nmols
    nreactions = args.nreactions
    nreactants = [int(x) for x in args.nreactants]
    nproducts = [int(x) for x in args.nproducts]
    rates = [float(x) for x in args.rates]
    
    #strip defaults
    if len(nreactants) > 1:
        nreactants = nreactants[1:]
    if len(nproducts) > 1:
        nproducts = nproducts[1:]
    if len(rates) > 1:
        rates = rates[1:]    
    
    rng = random.Random(args.seed)
    net = Uniform(nmols, nreactions, nreactants, nproducts, rates, rng=rng)
    
    chemstr = """#Uniform reaction network
# nmols = {0}
# nreactions = {1}
# reactants = {2}
# products = {3}
# rates = {4}
# seed = {5}
    
""".format(repr(nmols), repr(nreactions), repr(nreactants), repr(nproducts), repr(rates), args.seed)
    chemstr += str(net)
    chemstr += "\n"

    if args.outfile is None:
        #print to standard out
        sys.stdout.write(chemstr)
    else:
        #write to provided filename
        args.outfile.write(chemstr)
