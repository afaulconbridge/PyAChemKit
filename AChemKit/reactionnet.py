#! /bin/python
"""
Core for all ReactionNetwork classes

Of particular note are the alternative constructors of :class:`ReactionNetwork`,
:meth:`ReactionNetwork.from_file`, :meth:`ReactionNetwork.from_filename` and
:meth:`ReactionNetwork.from_string`.
"""

#regular expression to detect reaction when reading from string-based inputs
import re
#used to converge from_string into from_file paradigm
import StringIO

__module__ = "AChemKit.reactionnet"

from AChemKit.utils.simpledot import SimpleDot

class ReactionNetwork(object):
    """
    A dictionary of reactions where each key is a reaction
    composed of (tuple(sorted(reactants)), sorted(tuple(products))) and each
    value is the rate.

    ReactionNetwork objects are immutable and hashable.

    ReactionNetwork objects support __eq__ and __ne__, but none of the other
    rich comparison operators (__lt__, __le__, __gt__, __ge__).

    Different subclassess should be implemented to generate reaction networks on
    demand (artificial chemistries, etc) and provide additional functionallity,
    such as visualization or metrics.

    Can be cast to string to get a `.chem` representation.
    """
    _seen = None
    _reactions = None
    _dot = None
    _str = None
    _hash = None

    __module__ = "AChemKit.reactionnet"

    def __init__(self, rates):
        for rate in rates.values():
            assert rate > 0.0
        for reactants, products in rates:
            assert tuple(sorted(reactants)) == reactants
            assert tuple(sorted(products)) == products

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
        """
        reactionstring = ""
        reactants, products = reaction
        if reactants == products:
            return ""

        for reactantsstring in sorted([str(x) for x in reactants]):
            reactionstring += str(reactantsstring)+" + "
        #remove trailing " + "
        reactionstring = reactionstring[:-3]

        if rate == 1.0:
            reactionstring += "\t->\t"
        else:
            reactionstring += "\t-"+str(rate)+">\t"

        for productsstring in sorted([str(x) for x in products]):
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
        if other is None:
            return False
        if other.__class__ != self.__class__:
            return False
        if self.rates == other.rates:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self, other):
        if self._hash == None:
            self._hash = hash(tuple(sorted(self.rates.keys())))
        return self._hash

    @property
    def dot(self):
        """
        Property wrapper around :meth:`to_dot` to provide attribute-like access.
        """
        if self._dot is None:
            self._dot = self.to_dot()
        return self._dot

    def to_dot(self, names=None, rates=None, shown = (), hidden = ()):
        """
        Return a `.dot` format string constructed using a :class:`AChemKit.utils.simpledot.SimpleDot`
        view of this reaction network.

        Molecular species are shown as either full names, identifier numbers, or as blank circles.
        This is determined by the `names` parameter, which is a string indicating which to use:

        "full"
            This will use the full molecule name specified in the .chem file

        "id"
            This will use a shortened identifier of that molecules index in the
            :meth:`seen` tuple.

        "blank"
            This will not name any molecules, but will put an empty circle instead.

        A sub-set of the reaction network can be drawn using the `shown` and `hidden` parameters.

        Reactions involving only molecular species on the `hidden` list are not shown. Molecular
        species on the `hidden` list are not shown unless they are involved in a reaction with
        molecular species not on the `hidden` list, in which case the molecular species on the
        `hidden` list is unlabeled and shown as a point.

        The `shown` list in the inverse of the hidden list. If it is used, any molecular species
        not on the `shown` list is treated as being on the `hidden` list. If a molecular species
        is on both `shown` and `hidden` lists, the `hidden` lists wins.


        Catalysts (defined as molecules that are required for but unchanged by a reaction)
        are indicated with a grey line.

        Reversible reactions (defined as a pair of reactions where reactants of one are the
        products of the other and visa versa) are combined and indicated with double arrows
        resembling a diamond shape.


        """

        #implement shown as an inverse of hidden
        #maybe raise an exception if something is on both?
        if len(shown) > 0:
            hidden = list(hidden)
            for molspecies in self.seen:
                if molspecies not in shown and molspecies not in hidden:
                    hidden.append(molspecies)
            hidden = tuple(hidden)

        dot = SimpleDot()
        dot["node"] = {}
        dot["node"]["fontsize"] = 10.0
        #make it as small as possible
        dot["node"]["margin"] = "0.02,0.02"
        dot["node"]["height"] = 0.0
        dot["node"]["width"] = 0.3

        dot["edge"] = {}
        dot["edge"]["dir"] = "both" #this is required to annotate tails
        dot["edge"]["len"] = 0.25

        dot["graph"] = {}
        dot["graph"]["layout"] = "sfdp"
        #dot["graph"]["overlap"] = "prism"
        dot["graph"]["overlap"] = "false"
        #dot["graph"]["normalize":True}
        dot["graph"]["K"] = dot["edge"]["len"] #this is similar to edge:len

        molplot = self.seen
        reactplot = self.reactions
        if len(hidden) > 0:
            molplot = set((x for x in molplot if x not in hidden))
            reactplot = []
            for reactants, products in self.reactions:
                mols = set(reactants+products)
                #at least one of the reacants or products is not hidden
                if len(mols.difference(hidden)) > 1:
                    reactplot.append((reactants, products))
                    molplot.update(mols)

            molplot = sorted(tuple(molplot))
            reactplot = tuple(reactplot)


        #try to do something smart with names
        if names is None:
            if max((len(x) for x in molplot)) > 10:
                names = "id"
            else:
                names = "full"


        for molspecies in molplot:
            m_id = "M%d" % self.seen.index(molspecies)
            attribs = {}
            if names == "full":
                #should try to escape this
                attribs["label"] = str(molspecies)
            elif names == "id":
                pass
            elif names == "blank":
                attribs["label"] = " "
                attribs["shape"] = "circle"
            else:
                raise ValueError, 'names must be one of "full", "id", or "blank"'

            if molspecies in hidden:
                attribs["label"] = " "
                attribs["shape"] = "point"

            dot[m_id ] = attribs

        for reactants, products in reactplot:
            #if this is the second of a reversible reaction, then dont show it
            if (products, reactants) in self.reactions[:self.reactions.index((reactants, products))]:
                continue


            r_id = "R % d"% self.reactions.index((reactants, products))
            dot[r_id] = {"shape":"point"}

            if rates == True or (rates is None and self.rates[(reactants, products)] != 1.0):
                dot[r_id] = {"label":self.rates[(reactants, products)]}
                #make it inverted colors
                dot[r_id]["style"] = "filled"
                dot[r_id]["fontcolor"] = "white"
                dot[r_id]["fillcolor"] = "black"
                #do stuff to make shape work on more versions of graphviz
                #dot[r]["regular"] = "true"
                #dot[r]["shape"] = "polygon"
                dot[r_id]["shape"] = "box"
                #no need to have margins as big as the ovals
                dot[r_id]["margin"] = "0.01,0.01"
                dot[r_id]["width"] = "0.0"
                dot[r_id]["height"] = "0.0"

            for i in xrange(len(reactants)):
                reactant = reactants[i]
                m_id = "M % d" % self.seen.index(reactant)
                #see if this is a catalyst
                #remember to allow for multiple copies of the same molecular species
                #to act as a collective catalyst
                jth = reactants[:i+1].count(reactant)
                attribs = {"arrowtail":"invempty", "arrowhead":"none"}
                if jth <= products.count(reactant):
                    attribs["arrowtail"] = "none"
                    attribs["color"] = "grey"

                #if it is a reversible reaction, annotate arrows accordingly
                if (products, reactants) in self.reactions:
                    if attribs["arrowtail"] == "invempty":
                        attribs["arrowtail"] = "normalinvempty"
                #dictionary notation does not allow multiple parralel edges
                #therefore use the add method
                dot.add((m_id, r_id), attribs)

            for i in xrange(len(products)):
                product = products[i]
                m_id = "M % d" % self.seen.index(product)
                #see if this is a catalyst
                #remeber to allow for multiple copies of the same molecular species
                #to act as a collective catalyst
                jth = products[:i+1].count(product)
                if jth > reactants.count(product):
                    attribs = {"arrowtail":"none", "arrowhead":"normal"}
                    #if it is a reversible reaction, annotate arrows accordingly
                    if (products, reactants) in self.reactions:
                        attribs["arrowhead"] = "emptyinv"

                    #dictionary notation does not allow multiple parralel edges
                    #therefore use the add method
                    dot.add((r_id, m_id), attribs)
        return dot

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
    def from_file(cls, infile):
        """
        Alternative constructor that accepts a :class:`file` object (or equivalent).

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

