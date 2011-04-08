#! /bin/python

"""
Functions for testing properties of particular reaction networks.

These functions expect an object of class :py:class:`AChemKit.reactionnet.ReactionNetwork`
or subclass or something with an equivalent API. It does not enforce
this however, so you may use custom classes with the same API.

Some of these properties have logical prerequisites, but these are not tested
for explicitly.

"""

#some of these could be accelerated by moving the lambdas to dedicated functions?


import itertools

def has_synthesis(rn):
    """
    Tests for reactions where reactants combine to produce fewer products.

    May also be called a *combination reaction*.

    For example::

        A + B -> AB
        A + B + C -> AB + D

    """
    for thing in itertools.ifilter(lambda (reactants, products):len(products) < len(reactants), rn.reactions):
        return True

    return False


def has_decomposition(rn):
    """
    Tests for reactions where reactants combine to produce more products.

    For example::

        AB -> A + B
        AB + C -> A + B + C

    """
    for thing in itertools.ifilter(lambda (reactants, products):len(products) > len(reactants), rn.reactions):
        return True
    return False


def has_catalysis_direct(rn):
    """
    Tests for reactions where some species is both consumed and produced by the same reaction.

    For example::

        A + C -> B + C
        AB + C -> A + B + C

    """
    for thing in itertools.ifilter(lambda (reactants, products):len(set(reactants).intersection(products)) > 0, rn.reactions):
        return True
    return False


def has_reversible(rn):
    """
    Tests for a pair of reactions where the products of one is the reactants of the other and visa vera.

    For example::

        A + B -> AB
        AB -> A + B

    """
    for thing in itertools.ifilter(lambda (reactants, products):(products, reactants) in rn.reactions, rn.reactions):
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


def has_divergence(rn):
    """
    Tests for divergent reactions.
    
    Divergent reactions are where the same reactants have multiple possible collections of products.
    
    For example::

        AB + C -> ABC
        AB + C -> A + B + C
    """
    
    seen_reactants = set()
    for reactants, products in rn.reactions:
        if reactants in seen_reactants:
            return True
        else:
            seen_reactants.add(reactants)
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
