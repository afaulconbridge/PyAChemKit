#! /bin/python
"""
Functions that construct random :class:`ReactionNetwork` instances by various methods.


"""
import random
import itertools
import re


from reactionnet import ReactionNetwork


def combinations_with_replacement(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    for indices in itertools.product(range(n), repeat=r):
        if sorted(indices) == list(indices):
            yield tuple(pool[i] for i in indices)


__all__ = ["Uniform", "Linear"]

def Uniform(nmols, nreactions, nreactants, nproducts, rates = 1.0, cls = ReactionNetwork, rng = None):
    """
    Generates a random :class:`ReactionNetwork` by assigning reaction randomly between all molecular species.

    Arguments:

    nmols
        Number of molecules in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    .. note::

        :class:`ReactionNetwork` tracks molecules by their reactions, so if a molecule is not part of any reaction
        it will not appear at all e.g. in :meth:`seen`. This could lead to differences from `nmols`.

    nreactions
        Number of reaction in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    .. note::

        The value of `nreactions` is the number of times a reaction will be added to the :class:`ReactionNetwork`. If it
        is already in the :class:`ReactionNetwork`, it will be replaced. This can lead to :class:`ReactionNetwork` with less
        than `nreactions` reactions.

    nreactants
        Number of reactants for each reaction in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

        .. note::
            If this is a tuple/list it will be sampled for each reaction.

    nproducts
        Number of products for each reaction in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

        If this is None, then `nreactants` must be a tuple of (`nreactants`, `nproducts`) or a list of tuples.

        .. note::
            If this is a tuple/list it will be sampled for each reaction.

    rates
        Rate of each reaction in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

        .. note::
            If this is a tuple/list it will be sampled for each reaction.

    cls
        Alternative class to use for constructing the return rather than :class:`ReactionNetwork`.

    rng
        Random number generator to use. If not specifed, one will be generated at random.


    These arguments can be a single value or a tuple/list which will be uniformly sampled from.

    For example:

    ``Uniform(5,3,2,1)`` will generate 5 molecules with 3 reactions between them where each reaction has two reactants and one product.

    ``Uniform(5,3,(1,2), (1,2))`` will generate 5 molecules with 3 reactions between them where each reaction has one or two reactants and one or two products.

    ``Uniform(5,3,((2,1),(1,2)), None)`` will generate 5 molecules with 3 reactions between them where each reaction has either two reactants and one product or one reactant and two products.

    """

    if rng is None:
        rng = random.Random(random.random())

    try:
        nmols = rng.choice(nmols)
    except TypeError:
        pass

    try:
        nreactions = rng.choice(nreactions)
    except TypeError:
        pass

    try:
        #its a tuple not a generator because its the same variable name
        nreactants = [rng.choice(nreactants) for i in xrange(nreactions)]
    except TypeError:
        nreactants = itertools.repeat(nreactants, nreactions)

    if nproducts is None:
        #its a tuple not a generator because its the same variable name
        nproducts = [x[1] for x in nreactants]
        nreactants = [x[0] for x in nreactants]
    else:
        try:
            nproducts = [rng.choice(nproducts) for i in xrange(nreactions)]
        except TypeError:
            nproducts = itertools.repeat(nproducts, nreactions)

    try:
        rates = [rng.choice(rates) for i in xrange(nreactions)]
    except TypeError:
        rates = itertools.repeat(rates, nreactions)

    mols = ["M%d"%i for i in xrange(nmols)]
    outrates = {}
    for thisnreactants, thisnproducts, thisrate in zip(nreactants, nproducts, rates):

        reactants = [rng.choice(mols) for j in xrange(thisnreactants)]
        products = [rng.choice(mols) for j in xrange(thisnproducts)]
        reactants = sorted(reactants)
        products = sorted(products)
        reactants = tuple(reactants)
        products = tuple(products)

        outrates[(reactants, products)] = thisrate

    return cls(outrates)


def Linear(natoms, maxlength, pform, pbreak, directed = True, rates = 1.0, cls = ReactionNetwork, rng = None):
    """
    Generates a random :class:`ReactionNetwork` from molecules that are strings of atoms and can join together or break apart.

    Based on the paper Autocatalytic sets of proteins. 1986. Journal of Theoretical Biology 119:1-24 by Kauffman, Stuart A.  but without the explicit catalytic activity.


    Arguments:

    natoms
        Number of atoms to use. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    .. note::

        :class:`ReactionNetwork` tracks molecules by their reactions, so if a molecule is not part of any reaction
        it will not appear at all e.g. in :meth:`seen`.

    maxlength
        Maximum number of atoms in a molecule. If this is None, then they are unbounded; this might cause problems with a computational explosion. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    pform
        Probability that a pair of molecules will join together per orientation. Must be between 0 and 1. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    pbreak
        Probability that any pair of atoms will break. Must be between 0 and 1.

    directed
        If false, molecules have no intrinsic direction so AlphBeta is equivlanet to BetaAlpha.
        **NOT IMPLEMENTED**

    rates
        Rate of each reaction in the reaction network. Can be a single value or a tuple/list which will be uniformly sampled from (duplicates can be used to give a non-uniform distribution).

    cls
        Alternative class to use for constructing the return rather than :class:`ReactionNetwork`.

    rng
        Random number generator to use. If not specifed, one will be generated at random.

    """

    if rng is None:
        rng = random.Random(random.random())


    try:
        natoms = rng.choice(natoms)
    except TypeError:
        pass

    try:
        maxlength = rng.choice(maxlength)
    except TypeError:
        pass

    #make sure rates is a tuple
    try:
        rates = rng.choice(rates)
    except TypeError:
        rates = [rates]

    #these are lists not sets because sets have machine-dependant ordering, which prevents reproducibility for the same random seed.
    molecules = []
    new = []

    #create some inital atoms
    #of the form Abc where first letter is capitalized
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for i in xrange(natoms):
        name = alpha[i%len(alpha)]
        while i >= len(alpha):
            i /= len(alpha)
            name = alpha[(i%len(alpha))-1] + name
        name = name.strip().capitalize()
        new.append(name)

    outrates = {}

    def mol_to_atoms(mol):
        return tuple(filter(lambda x: len(x) > 0, re.split(r"([A-Z][a-z]*)", mol)))

    def mol_len(mol):
        #return len(mol)
        return len(mol_to_atoms(mol))

    def mol_reverse(mol):
        rmol = ""
        for atom in mol_to_atoms(mol):
            rmol = atom + rmol
        return rmol

    def mol_order(mol):
        rmol = mol_reverse(mol)
        if mol < rmol:
            return mol
        else:
            return rmol

    def atoms_to_mol(atoms):
        mol = ""
        for atom in atoms:
            mol = mol + atom
        return mol


    while len(new) > 0:
        oldnew = new
        new = []
        #decomposition
        for z in oldnew:
            for i in xrange(1, mol_len(z)):
                if rng.random() < pbreak:
                    a = atoms_to_mol(mol_to_atoms(z)[:i])
                    b = atoms_to_mol(mol_to_atoms(z)[i:])

                    if not directed:
                        a = mol_order(a)
                        b = mol_order(b)

                    reaction = ((z,), tuple(sorted((a,b))))

                    if reaction not in outrates:
                        outrates[reaction] = 0.0
                    outrates[reaction] += rng.choice(rates)

                    if a not in molecules and a not in new:
                        new.append(a)
                    if b not in molecules and b not in new:
                        new.append(b)

        for a, b in itertools.chain(itertools.product(oldnew, molecules), combinations_with_replacement(oldnew, 2)):
            if maxlength is None or mol_len(a) + mol_len(b) <= maxlength:

                combinations = ((a,b), (b,a))
                if not directed:
                    combinations += ((mol_reverse(a), b), (a, mol_reverse(b)))

                for x,y in combinations:
                    if rng.random() < pform:
                        z = x + y

                        if not directed:
                            z = mol_order(z)

                        #because we may have revereed them, we have to oder them again
                        if not directed:
                            reactants = tuple(sorted((mol_order(x), mol_order(y))))
                        else:
                            reactants = tuple(sorted((x, y)))
                        products = tuple(sorted((z,)))

                        reaction = (reactants, products)

                        if reaction not in outrates:
                            outrates[reaction] = 0.0

                        outrates[reaction] += rng.choice(rates)

                        if z not in molecules and z not in new:
                            new.append(z)
        for z in oldnew:
            molecules.append(z)

    return cls(outrates)
