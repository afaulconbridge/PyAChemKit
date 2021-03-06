from achemkit import ReactionNetwork
from achemkit import SimpleDot

class ReactionNetworkDot(ReactionNetwork):
    """
    This is a subclass of :py:class:`achemkit.reactionnet.ReactionNetwork` 
    that adds a `.dot` representation. It is in a subclass so that on
    machines where dot is not installed, the basic class can still be
    used.
    """
    
    def __init__(self, *args, **kwargs):
        super(ReactionNetworkDot, self).__init__(*args, **kwargs)

    @property
    def dot(self):
        """
        Property wrapper around :py:meth:`~achemkit.reactionnetdot.ReactionNetworkDot.to_dot` to provide attribute-like access.
        """
        if self._dot is None:
            self._dot = self.to_dot()
        return self._dot

    def to_dot(self, names=None, rates=None, shown=(), hidden=()):
        return net_to_dot(self, names, rates, shown, hidden)

def net_to_dot(net, names=None, rates=None, shown=(), hidden =()):
    """
    Return a `.dot` format string constructed using a :py:class:`achemkit.utils.simpledot.SimpleDot`
    view of this reaction network.

    Molecular species are shown as either full names, identifier numbers, or as blank circles.
    This is determined by the `names` parameter, which is a string indicating which to use:

    "full"
        This will use the full molecule name specified in the .chem file

    "id"
        This will use a shortened identifier of that molecules index in the
        :py:attr:`~achemkit.reactionnet.ReactionNetwork.seen` tuple.

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
        for molspecies in net.seen:
            if molspecies not in shown and molspecies not in hidden:
                hidden.append(molspecies)
        hidden = tuple(hidden)

    dot = SimpleDot()
    #Override some dot defaults to get better looking graphs
    dot["node"] = {}
    dot["node"]["fontsize"] = 10.0
    #make it as small as possible
    dot["node"]["margin"] = "0.02,0.02"
    dot["node"]["height"] = 0.0
    dot["node"]["width"] = 0.3
    dot["node"]["shape"] = "box"

    dot["edge"] = {}
    dot["edge"]["dir"] = "both" #this is required to annotate tails
    dot["edge"]["len"] = 0.4
    dot["edge"]["K"] = 0.4

    dot["graph"] = {}
    #dot["graph"]["layout"] = "sfdp"
    #dot["graph"]["overlap"] = "prism"
    dot["graph"]["overlap"] = "false"
    dot["graph"]["normalize"] = "true"
    dot["graph"]["splines"] = "true"
    dot["graph"]["nodesep"] = 0.2
    dot["graph"]["ranksep"] = 0.15
    dot["graph"]["K"] = dot["edge"]["len"] #this is similar to edge:len

    molplot = net.seen
    reactplot = net.reactions
    if len(hidden) > 0:
        molplot = set((x for x in molplot if x not in hidden))
        reactplot = []
        for reactants, products in net.reactions:
            mols = set(reactants+products)
            #at least one of the reacants or products is not hidden
            if len(mols.difference(hidden)) > 1:
                reactplot.append((reactants, products))
                molplot.update(mols)

        molplot = sorted(tuple(molplot))
        reactplot = tuple(reactplot)


    #try to do something smart with names
    if names is None:
        if len(molplot) > 0 and max((len(str(x)) for x in molplot)) > 10:
            names = "id"
        else:
            names = "full"


    for molspecies in molplot:
        m_id = "M%d" % net.seen.index(molspecies)
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
        if (products, reactants) in net.reactions[:net.reactions.index((reactants, products))]:
            continue


        r_id = "R%d" % net.reactions.index((reactants, products))
        dot[r_id] = {"label":"   "}
        #make it inverted colors
        dot[r_id]["style"] = "filled"
        dot[r_id]["fontcolor"] = "white"
        dot[r_id]["fillcolor"] = "black"
        if (products, reactants) in net.reactions:
            dot[r_id]["shape"] = "point"
            dot[r_id]["margin"] = "0.0,0.0"
            dot[r_id]["width"] = "0.0"
            dot[r_id]["height"] = "0.0"
        else:
            dot[r_id]["shape"] = "box"
            #no need to have margins as big as the ovals
            dot[r_id]["margin"] = "0.01,0.01"
            dot[r_id]["width"] = "0.2"
            dot[r_id]["height"] = "0.2"

        if rates == True or (rates is None and net.rate(reactants, products) != 1.0):
            dot[r_id]["label"] = net.rate(reactants, products)

        for i in xrange(len(reactants)):
            reactant = reactants[i]
            m_id = "M%d" % net.seen.index(reactant)
            #see if this is a catalyst
            #remember to allow for multiple copies of the same molecular species
            #to act as a collective catalyst
            jth = reactants[:i+1].count(reactant)
            attribs = {"arrowtail":"invempty", "arrowhead":"none"}
            if jth <= products.count(reactant):
                attribs["arrowtail"] = "none"
                attribs["color"] = "grey"

            #if it is a reversible reaction, annotate arrows accordingly
            if (products, reactants) in net.reactions:
                if attribs["arrowtail"] == "invempty":
                    attribs["arrowtail"] = "normalinvempty"
            #dictionary notation does not allow multiple parralel edges
            #therefore use the add method
            dot.add((m_id, r_id), attribs)

        for i in xrange(len(products)):
            product = products[i]
            m_id = "M%d" % net.seen.index(product)
            #see if this is a catalyst
            #remeber to allow for multiple copies of the same molecular species
            #to act as a collective catalyst
            jth = products[:i+1].count(product)
            if jth > reactants.count(product):
                attribs = {"arrowtail":"none", "arrowhead":"normal"}
                #if it is a reversible reaction, annotate arrows accordingly
                if (products, reactants) in net.reactions:
                    attribs["arrowhead"] = "emptyinv"

                #dictionary notation does not allow multiple parralel edges
                #therefore use the add method
                dot.add((r_id, m_id), attribs)
    return dot
