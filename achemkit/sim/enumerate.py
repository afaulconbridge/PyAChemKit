import itertools

from achemkit.utils.bag import OrderedFrozenBag


def enumerate(achem, mols, maxdepth=None, maxmols=None):
    """
    Generates a reaction network using a function that returns all possible products 
    for a given set of reactants and an initial set of molecules.
    
    allreactions is a function that takes two reactants as parameters, (typically
    via *args) and returns a dictionary of possible outcomes and their weighting.
    
    maxdepth is the number of times all reactions of seen molecules is evaluated. If it 
    is None, then the process repeats until no more novel molecules are created; this
    may lead to an infinite loop.
    """
    #make sure mols are unique
    newmols = sorted(list(set(mols)))
    mols = list()
    rates = {}
    i = 0
    allreactants = set()
    
    while (maxdepth is None or i < maxdepth)\
            and (maxmols is None or len(mols)+len(newmols) < maxmols)\
            and len(newmols) > 0:
        newnewmols = []
        
        def molcombos(mols, newmols):
            for a in mols+newmols:
                for b in newmols:
                    if a in newmols and newmols.index(b) < newmols.index(a):
                        continue
                    yield a,b
             
        results = map(achem.all_reactions, molcombos(mols, newmols))
            
        for args, abrates in itertools.izip(molcombos(mols, newmols), results):
            a,b = args
            abrates = dict(abrates)
            assert abrates is not None
            #print i, len(mols) + len(newmols) + len(newnewmols), maxmols
            if maxmols is not None and len(mols) + len(newmols) + len(newnewmols) > maxmols:
                break
            for reaction in abrates:
                rate = abrates[reaction]
                reactants, products = reaction
                reactants = OrderedFrozenBag(reactants)
                products = OrderedFrozenBag(products)
                reaction = reactants, products
                
                if reactants != products:
                    for mol in products:
                        if mol not in mols and mol not in newmols and mol not in newnewmols:
                            newnewmols.append(mol)
                                
                    assert reaction not in rates
                    rates[reaction] = rate
                    
                    yield (0.0, reactants, products)
        mols.extend(newmols)
        mols = sorted(mols)
        newmols = sorted(newnewmols)
        i += 1
    
