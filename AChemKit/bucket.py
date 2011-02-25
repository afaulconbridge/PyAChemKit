"""
Library for working with `buckets`; instances of a simulation of an Artificial Chemistry. 

Various tools for going between ReactionNetwork  and Buckets, as well an analysing buckets.


"""

import re

from reactionnet import ReactionNetwork





class Event(object):
    """
    Mini-class for tracking events (instances of a reaction) within a bucket.

    Supports comparisons, is hashable, is immutable
    """

    def __init__(self, time, reactants, products):
        self.time = time
        self.reactants = tuple(sorted(list(reactants)))
        self.products = tuple(sorted(list(products)))

    def __eq__(self, other):
        if self.time == other.time and self.reactants == other.reactants and self.products == other.products:
            return True
        return False

    def __ne__(self, other):
        if self.time == other.time and self.reactants == other.reactants and self.products == other.products:
            return False
        return True

    def __lt__(self, other):
        if self.time < other.time:
            return True
        return False

    def __le__(self, other):
        if self == other or self.time < other.time:
            return True
        return False

    def __gt__(self, other):
        if self.time > other.time:
            return True
        return False

    def __ge__(self, other):
        if self == other or self.time > other.time:
            return True
        return False

    def __hash__(self):
        if self._hash == None:
            self._hash = hash(self.time) + hash(self.reactants) + hash(self.products)
        return self._hash

class Bucket(object):
    """
    Event history of a simulation of an Artificial Chemistry.
    """
    _reactionnet = None

    def __init__(self, events):
        self.events = tuple(sorted(list(events)))

    @classmethod
    def from_string(cls, instr):
        """
        Wrapper around :meth:`from_file` that uses :class:`~StringIO.StringIO`.
        """
        return cls.from_file(StringIO.StringIO(instr))

    @classmethod
    def from_filename(cls, infilename):
        """
        Wrapper around :meth:`from_file` that opens the provided filename as a file to read.
        """
        return cls.from_file(open(infilename, "r"))

    @classmethod
    def from_file(cls, file):
        """
        Alternative constructor that accepts a :class:`file` object (or equivalent).

        Source must be formatted as a bucket log  file, see :ref:`bucket_file_format`.
        """
        events = []
        for line in file:
            line = line.strip()
            
            splitted = line.split()
            if len(splitted) < 3:
                raise ValueError, "invalid reaction: "+reaction
            
            walltime = splitted[0]
            simtime = splitted[1]
            reaction = " ".join(splitted[2:])
            
            walltime = int(walltime)
            simtime = float(simtime)

            match = re.search(r"^(.*?)->(.*?)$", reaction)
            
            if match == None:
                raise ValueError, "invalid reaction: "+reaction
                
            reactants, products = match.groups()

            reactants = reactants.split("+")
            reactants = tuple(sorted( [x.strip() for x in reactants if len(x.strip()) > 0] ))

            products = products.split("+")
            products = tuple(sorted( [x.strip() for x in products if len(x.strip()) > 0] ))

            for reactant in reactants:
                assert " " not in reactant
                assert "\t" not in reactant
                assert "->" not in reactant
            for product in products:
                assert " " not in product
                assert "\t" not in product
                assert "->" not in product

            event = Event(simtime, reactants, products)
            events.append(event)
        return cls(events)

    @property
    def reactionnet(self):
        if self._reactionnet == None:
            #need to create a rates structure, then convert it to a reactionnet
            rates = {}
            for event in self.events:
                reaction = (event.reactants, event.products)
                if reaction not in rates:
                    rates[reaction] = 0
                rates[reaction] += 1
                #if event.reactants == event.products:
                #    print "Bounce"

            #should correct the rates by the total number of collisions of those reactants
            #BUT current old data does not track bounces :`(

            self._reactionnet = ReactionNetwork(rates)

        return self._reactionnet
