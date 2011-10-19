"""
Various functions that interact with NetworkX (http://networkx.lanl.gov/)

This is used because its a fast graph library with lots of nice algorithms in it.
"""
import re
import itertools

import networkx

from achemkit import ReactionNetwork
from achemkit.utils.utils import long_subseq
from achemkit import properties

def make_linkage_graph(rn):
    """
    For each reactant and each product in each reaction, they are linked.
    """
    G = networkx.MultiDiGraph()
    for reaction in rn.reactions:
        reactants, products = reaction
        #remove catalysts
        reactants = list(reactants)
        products = list(products)
        catalysts = set(reactants).intersection(products)
        
        for reactant in reactants:
            for product in products:
                if reactant != product and reactant not in catalysts and product not in catalysts:
                    G.add_edge(reactant, product, reaction = rn.reaction_to_string(reaction, rn.rate(*reaction)))
    return G
    
def make_similar_linkage_graph(rn, similar_func, G=None):
    """
    For each reactant and each product in each reaction, they are linked
    if the similar_func return true.
    """
    if G is None:
        G = make_linkage_graph(rn)
    else:
        G = copy.copy(G)
    for edge in G.edges():
        if not similar_func(edge):
            G.remove_edge(*edge)
    return G

def make_catalysis_graph(rn):
    """
    For each reactant and each product in each reaction, they are linked
    if the reactant is a catalsyst.
    
    This Will never form self-edges.
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
        #assert len(catalysts) == 1
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
    
def find_cycles(net, G = None):
    if G is None:
        G = make_catalysis_graph(net)
    return _find_cycles_or_loop(G)


def find_loops(net, similar_func, G = None):
    if G is None:
        G = make_similar_linkage_graph(net, similar_func)
    loops = _find_cycles_or_loop(G)
    loops = [x for x in filter_loops(loops) if similar_func(x)]
    return loops


def _find_cycles_or_loop(G):
    cycles = set()
    for edge in G.edges():
        nG = G
        try:
            cycle = networkx.algorithms.shortest_path(nG, edge[1], edge[0])
            #should get all shrotest paths rather than A shortest path.
        except networkx.exception.NetworkXNoPath:
            cycle = None
            
        if cycle is not None:
            #there is a cycle
            #there could be more than one cycle, this just finds the shortest
            #probably what we actually want in most cases
            #put the cycle starting at the minimum
            start = min(cycle)
            i = cycle.index(start)
            cycle = cycle[i:] + cycle[:i]
            cycle = tuple(cycle)
            
            if cycle not in cycles:
                cycles.add(cycle)
    return sorted(list(cycles))
            
def filter_loops(loops):
    """
    Filters the itterable of loops according to which loops contain other.
    
    Only yield those loops which are not contained within other loops.
    
    Provided itterable is converted to list internally.
    """
    loops = sorted(loops, lambda x, y: cmp(len(x), len(y)), reverse=True)
        
    for loop in itertools.imap(_filter_loops, xrange(len(loops)), [loops]*len(loops)):
        if loop is not None:
            yield loop
            
def _filter_loops(i, loops):
    """
    Internal function used by filter_loops
    """
    
    def loop_contains(a, b):
        if not set(a) >= set(b):
            return False

        a = a+a
        for i in xrange(len(b)):
            b_test = b[i:]+b[:i]
            for j in xrange(len(a)-len(b)):
                if a[j:j+len(b)] == b_test:
                    return True
        return False
        
    contains = False
    for j in xrange(i+1, len(loops)):
        if i != j and len(loops[j]) < len(loops[i]) and loop_contains(loops[i], loops[j]):
	        contains = True
	        break
    if not contains:
        return loops[i]
