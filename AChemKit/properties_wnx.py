"""
Various functions that interact with NetworkX (http://networkx.lanl.gov/)

This is used because its a fast graph library with lots of nice algorithms in it.
"""
import re
import itertools

import networkx

from . import reactionnet
from .utils.utils import long_subseq
from . import properties

def make_linkage_graph(rn, min_shared = 3):
    """
    For each reactant and each product in each reaction, they are linked
    if they share at minimum subsequence length.
    """
    G = networkx.MultiDiGraph()
    for reaction in rn.reactions:
        reactants, products = reaction
        for reactant in reactants:
            for product in products:
                if reactant != product and len(long_subseq((reactant, product))) >= min_shared:
                    G.add_edge(reactant, product, reaction = rn.reaction_to_string(reaction, rn.rate(*reaction)))
    return G

def make_catalysis_graph(rn, min_shared = 3):
    """
    For each reactant and each product in each reaction, they are linked
    if they share at minimum subsequence length and if the reactant
    is a catalsyst.
    """
    G = networkx.MultiDiGraph()
    for reaction in properties.get_catalysis_direct(rn):
        reactants, products = reaction
        #remove an equal number of each catalysts from reactants and products
        #convert to a list
        reactants = list(reactants)
        products = list(products)
        #work out what the catalysts are
        #probably only one of them
        catalysts = set(reactants).intersection(products)
        assert len(catalysts) == 1
        assert len(catalysts) > 0
        for catalyst in catalysts:
            count = min(reactants.count(catalyst), products.count(catalyst))
            assert count > 0
            for i in xrange(count):
                reactants.remove(catalyst)
                products.remove(catalyst)
        
        for catalsyst in catalysts:
            for product in products:
                G.add_edge(catalsyst, product, reaction = rn.reaction_to_string(reaction, rn.rate(*reaction)))
    return G
