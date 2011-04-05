#! /bin/python
"""
Core for all ReactionNetwork classes

Of particular note are the alternative constructors of :py:class:`~AChemKit.reactionnet.ReactionNetwork`,
:py:meth:`~AChemKit.reactionnet.ReactionNetwork.from_file`, :py:meth:`~AChemKit.reactionnet.ReactionNetwork.from_filename` and
:py:meth:`~AChemKit.reactionnet.ReactionNetwork.from_string`.
"""

#regular expression to detect reaction when reading from string-based inputs
import re
#used to converge from_string into from_file paradigm
import StringIO


class ReactionNetwork(object):
    """
    A dictionary of reactions where each key is a reaction
    composed of (reactants, products) and each
    value is the rate.

    :py:class:`~AChemKit.reactionnet.ReactionNetwork` objects are immutable and hashable.

    :py:class:`~AChemKit.reactionnet.ReactionNetwork` objects support :py:meth:`~AChemKit.reactionnet.ReactionNetwork.__eq__` and :py:meth:`~AChemKit.reactionnet.ReactionNetwork.__ne__`, but none of the other
    rich comparison operators (__lt__, __le__, __gt__, __ge__).

    Different subclassess could be implemented to generate reaction networks on
    demand (artificial chemistries, etc) and provide additional functionallity,
    such as visualization or metrics.

    Can be cast to string to get a `.chem` representation.
    """
    _seen = None
    _reactions = None
    _dot = None
    _str = None
    _hash = None

    def __init__(self, rates):
        for rate in rates.values():
            assert rate > 0.0
        self.rates = rates

    @property
    def seen(self):
        """
        Sorted tuple of all molecular species in the network
        """
        if self._seen is None:
            self._seen = set()
            for reactants, products in self.rates:
                self._seen.update(reactants)
                self._seen.update(products)
            self._seen = tuple(sorted(self._seen))
        return self._seen

    @property
    def reactions(self):
        """
        Sorted tuple of all reactions in the network
        """
        if self._reactions is None:
            self._reactions = tuple(sorted(self.rates.keys()))
        return self._reactions
    
    @classmethod
    def reaction_to_string(cls, reaction, rate=1.0):
        """
        Produces a human-readable string for a particular reaction.
        
        Mainly used to convert entire reaction network to a string representation,
        but can also be used for individual reactions if desired.
        """
        reactionstring = ""
        reactants, products = reaction
        if reactants == products:
            return ""

        for reactantsstring in [str(x) for x in reactants]:
            reactionstring += str(reactantsstring)+" + "
        #remove trailing " + "
        reactionstring = reactionstring[:-3]

        if rate == 1.0:
            reactionstring += "\t->\t"
        else:
            reactionstring += "\t-"+str(rate)+">\t"

        for productsstring in [str(x) for x in products]:
            reactionstring += productsstring+" + "
        #remove trailing " + "
        reactionstring = reactionstring[:-3]
        return reactionstring
        

    def __str__(self):
        if self._str is None:
            reactionstrings = []
            for reaction in self.reactions:
                reactionstr = self.reaction_to_string(reaction, self.rates[reaction])
                if reactionstr != "":
                    reactionstrings.append(reactionstr)

            reactionstrings.sort()
            self._str = ""
            for reaction in reactionstrings:
                self._str += reaction
                if reaction is not reactionstrings[-1]:
                    self._str += "\n"
        return self._str

    def __eq__(self, other):
        """
        Two instances of :py:class:`~.ReactionNetwork` are equal if and 
        only if the :py:meth:`~.ReactonNetwork.rates` are equal.
        """
        if other is None:
            return False
        if other.__class__ != self.__class__:
            return False
        if self.rates == other.rates:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Two instances of :py:class:`~.ReactionNetwork` are equal if and 
        only if the :py:meth:`~.ReactonNetwork.rates` are equal.
        """
        return not self.__eq__(other)

    def __hash__(self):
        if self._hash == None:
            self._hash = hash(tuple(sorted(self.rates.keys())))+hash(tuple(sorted(self.rates.values())))
        return self._hash

    @classmethod
    def from_string(cls, instr):
        """
        Wrapper around :py:meth:`AChemKit.reactionnet.ReactionNetwork.from_file` that uses :class:`~StringIO.StringIO`.
        """
        return cls.from_file(StringIO.StringIO(instr))

    @classmethod
    def from_filename(cls, infilename):
        """
        Wrapper around :py:meth:`AChemKit.reactionnet.ReactionNetwork.from_file` that opens the provided filename as a file to read.
        """
        return cls.from_file(open(infilename, "r"))

    @classmethod
    def from_file(cls, infile):
        """
        Alternative constructor that accepts a :py:func:`file` object (or equivalent).

        Source must be formatted as a .chem file, see :ref:`chem_file_format`.
        """
        rates = {}
        linecount = 0
        repattern = r'-([0-9]*\.?[0-9]*)>'
        for line in infile:
            #keep a copy of the line for printout in case of problem
            rawline = line
            line = line.strip()
            #record which line of the file we are on for
            #printout in case of problem
            linecount += 1
            #ignore comments and blanks
            if len(line) == 0 or line[0] == "#":
                pass
            elif re.search(repattern, line) != None:
                #A -> B
                #A + B -> C
                #A+ B -> C
                #A -2> B
                # A -2.0> B
                splitline = re.split(repattern, line)

                if len(splitline) != 3:
                    raise ValueError, "Invalid reaction at line %d : %s" % (linecount, rawline)

                inputstring, rate, outputstring = splitline

                if len(rate):
                    rate = float(rate)
                else:
                    rate = 1.0

                inputs = []
                for molspecies in inputstring.split('+'):
                    molspecies = molspecies.strip()
                    if len(molspecies):
                        inputs.append(molspecies)

                outputs = []
                for molspecies in outputstring.split('+'):
                    molspecies = molspecies.strip()
                    if len(molspecies):
                        outputs.append(molspecies)

                inputs.sort()
                inputs = tuple(inputs)

                outputs.sort()
                outputs = tuple(outputs)

                if (inputs, outputs) in rates:
                    #raise ValueError, "Duplicate reaction at line %d : %s" % (linecount, rawline)
                    break

                if inputs == outputs:
                    #raise ValueError, "Invalid reaction at line %d : %s" % (linecount, rawline)
                    break

                rates[(inputs, outputs)] = rate

            else:
                raise ValueError, "Invalid reaction at line %d : %s" % (linecount, rawline)
        return ReactionNetwork(rates)
