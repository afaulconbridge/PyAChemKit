"""
Various functions that interact with NetworkX (http://networkx.lanl.gov/)

This is used because its a fast graph library with lots of nice algorithms in it.
"""
import re
import itertools

import networkx

from . import reactionnet
from .utils.utils import long_subseq

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
                    G.add_edge(reactant, product, reaction = rn.reaction_to_string(reaction, rn.rates[reaction]))
    return G

def make_catalysis_graph(rn, min_shared = 3):
    """
    For each reactant and each product in each reaction, they are linked
    if they share at minimum subsequence length and if the reactant
    is a catalsyst.
    """
    G = networkx.MultiDiGraph()
    for reaction in rn.reactions:
        reactants, products = reaction
        for reactant in reactants:
            if products.count(reactant) >= reactants.count(reactant):
                for product in products:
                    if reactant != product and len(long_subseq((reactant, product))) >= min_shared:
                        G.add_edge(reactant, product, reaction = rn.reaction_to_string(reaction, rn.rates[reaction]))
    return G
