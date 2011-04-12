"""
Functions for testing properties of particular reaction networks.

These functions expect an object of class :py:class:`AChemKit.reactionnet.ReactionNetwork`
or subclass or something with an equivalent API. It does not enforce
this however, so you may use custom classes with the same API.

Some of these properties have logical prerequisites, but these are not tested
for explicitly.

"""
import itertools

#some of these could be accelerated by moving the lambdas to dedicated functions?


def get_synthesis(rn):
    """
    Returns all reactions where reactants combine to produce fewer products.

    May also be called a *combination reaction*.

    For example::

        A + B -> AB
        A + B + C -> AB + D
        
    Works as an iterator filter.
    """
    for reaction in itertools.ifilter(lambda (reactants, products):len(products) < len(reactants), rn.reactions):
        yield reaction

def has_synthesis(rn):
    "Tests if any reactions are synthesis. See :py:func:`~get_synthesis` for definition."
    for reaction in get_synthesis(rn):
        return True
    return False

def get_decomposition(rn):
    """
    Returns all reactions where reactants combine to produce more products.

    For example::

        AB -> A + B
        AB + C -> A + B + C

    Works as an iterator filter.
    """
    for reaction in itertools.ifilter(lambda (reactants, products):len(products) > len(reactants), rn.reactions):
        yield reaction

def has_decomposition(rn):
    "Tests if any reactions are decomposition. See :py:func:`~get_decomposition` for definition."
    for reaction in get_decomposition(rn):
        return True
    return False


def get_catalysis_direct(rn):
    """
    Tests for reactions where some species is both consumed and produced by the same reaction.

    For example::

        A + C -> B + C
        AB + C -> A + B + C

    """
    for reaction in itertools.ifilter(lambda (reactants, products):len(set(reactants).intersection(products)) > 0, rn.reactions):
        yield reaction

def has_catalysis_direct(rn):
    "Tests if any reactions are direct catalysis. See :py:func:`~get_catalysis_direct` for definition."
    for reaction in get_catalysis_direct(rn):
        return True
    return False


def get_autocatalysis_direct(rn):
    """
    Tests for reactions where some species is both consumed and produced by the same reaction, and is produced more than 
    it is consumed.

    For example::

        A + C -> A + A

    """
    for reaction in get_catalysis_direct(rn):
        reactants, products = reaction
        for reactant in reactants:
            if products.count(reactant) > reactants.count(reactant):
                yield reaction
                break #stop looking at reactants

def has_autocatalysis_direct(rn):
    "Tests if any reactions are direct autocatalysis. See :py:func:`~get_autocatalysis_direct` for definition."
    for reaction in get_autocatalysis_direct(rn):
        return True
    return False
    

def get_reversible(rn):
    """
    Tests for a pair of reactions where the products of one is the reactants of the other and visa vera.

    For example::

        A + B -> AB
        AB -> A + B

    """
    for reaction in itertools.ifilter(lambda (reactants, products):(products, reactants) in rn.reactions, rn.reactions):
        yield reaction

def has_reversible(rn):
    "Tests if any reactions are reversible. See :py:func:`~get_reversible` for definition."
    for reaction in get_reversible(rn):
        return True
    return False


def get_divergence(rn):
    """
    Tests for divergent reactions.
    
    Divergent reactions are where the same reactants have multiple possible collections of products.
    
    For example::

        AB + C -> ABC
        AB + C -> A + B + C
    """
    reactions = list(rn.reactions)
    for i in xrange(len(reactions)):
        reaction = reactions[i]
        for j in xrange(i+1, len(reactions)):
            if reactions[j][0] == reaction[0]:
                yield reaction
                break
    
def has_divergence(rn):
    "Tests if any reactions are divergent. See :py:func:`~get_divergence` for definition."
    for reaction in get_divergence(rn):
        return True
    return False


def has_varying_rates(rn):
    """
    Tests that the reaction network has different rates for different reactions.

    To get the range of rates a reaction network spans, use::

        span = max(rn.rates.values())-min(rn.rates.values())
    """
    if len(set(rn.rates.values())) > 1:
        return True
    return False


def not_conservation_mass(rn):
    """
    Tests for violation of conservation of mass.

    Note, we can show that a reaction network breaks conservation of mass, but not prove that it obeys it.

    This is done by arranging all the molecules into a partially ordered set - a tree from largest to smallest. If this
    cannot be done, then conservation of mass must be violated. If this can be done, then conservation of mass may or may
    not apply - it cannot be said for certain.

    This requires that each molecular species can be separated into individual atoms. If this is not possible, then
    this function will not work.

    NEEDS TO BE WRITTEN

    (Credit to Adam Nellis for algorithm)
    """

    return False
