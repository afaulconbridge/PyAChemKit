"""
A library to manage `.dot` files

There are existing python libraries for this, but they do not
always do it correctly (e.g. PyDot does not respect order within
a .dot file).
"""

#this is required for the rendering
import subprocess

#required to easily enable dictionary-like access
#Starting with Python version 2.6, it is recommended to use
#collections.MutableMapping instead of DictMixin
#could also subclass dict directly
from UserDict import DictMixin

class SimpleDot(DictMixin):
    """
    Repsents a graphviz `.dot` file (also known as `.gv`).

    Uses a dictionary-like interface via the :class:~`UserDict.DictMixin`
    class.

    To produce `.dot` output, cast to string e.g. `str(mysimpledot)`

    Contains three types of graph objects:

    Nodes
        Named by strings and are dictionaries of attributes.

    Edges
        Named by tuples of length 2 of strings and are are
        dictionaries of attributes. Nodes will be implicitly created by
        graphviz if they do not exist, and therefore do not need to be
        explicitly created.

    Subgraphs
        Named by strings and are instances of this class. Some
        graphviz layout engines (e.g. `neato`) will flatten subgraphs.

    These can be set and accessed by standard slice notation (e.g.
    `dot[nodename] = {}`).

    Node names and subgraph names are unique but multiple parallel edges
    are permitted. However, slice notation (e.g. `dot[(from, to)]`) cannot
    cope with this. Therefore, when there are multiple parallel edges,
    accessing any of them returns a tuple of all their attributes as
    dictionaries. To create multiple parallel edges you must use the
    :meth:`add` method

    Names of nodes and subgraphs, attribute keys, and attribute values
    should all be graphviz compatible. Some attempt to wrap string attribute
    values in quotes will be made so that the use of plain python strings
    is accepted by graphviz.

    Very little checking and enforcement is performed. This means that you
    can use them in ways not originally intended; for example, you can
    se attributes that no graphviz programme will recognize. But, it also
    means you can break it by doing odd things to them.

    """
    name = None
    content = None
    digraph = True
    strict = False
    cluster = False

    def __init__(self, name="G", digraph=True, strict=False, cluster=False):
        self.name = name
        self.digraph = digraph
        self.strict = strict
        self.cluster = cluster
        self.prefix = ""
        self.content = []
        self.keylist = []

        #content is a list of names of things
        #nodes are a string
        #edges are tuples of length two (from, to)
        #subgraphs are a SimpleDot object

    def keys(self):
        """
        Return a tuple of the keys.
        """
        return tuple(self.keylist)

    def __getitem__(self, key):
        if key not in self.keylist:
            self[key] = {}
            return self[key]
        elif self.keylist.count(key) > 1:
            #there may be multiple edges in the same graph
            return tuple((self.content[i] for i in xrange(len(self.keylist)) if self.keylist[i] == key))
        else:
            return self.content[self.keylist.index(key)]

    def __setitem__(self, key, value):
        if key not in self.keylist:
            self.add(key, value)
        elif self.keylist.count(key) > 1:
            raise TypeError, "setitem cannot be used with multi-use keys"
        else:
            self.content[self.keylist.index(key)] = value

    def __delitem__(self, key):
        if key not in self.keylist:
            raise KeyError
        elif self.keylist.count(key) > 1:
            raise IndexError, "delitem cannot be used with multi-use keys"
        else:
            self.content.pop(self.keylist.index(key))
            self.keylist.pop(self.keylist.index(key))

    def add(self, key, value=None):
        """
        Guaranteed to add the passed key/value to self, even if it is a duplicate.
        """
        if value is None:
            value = {}
        self.keylist.append(key)
        self.content.append(value)

    def get(self, key):
        """
        Returns a tuple of all things matching that key.

        Designed for multiple edges, but will also work with single edges, nodes, or subgraphs.
        This provides a unified interface.
        """
        return tuple((self.content[i] for i in xrange(len(self.keylist)) if self.keylist[i] == key))

    def __delitem__(self, key):
        if key not in self.keylist:
            raise KeyError
        elif self.keylist.count(key) > 1:
            raise TypeError, "delete cannot be used with multi-use keys"
        else:
            i = self.keylist.index(key)
            del self.keylist[i]
            del self.content[i]

    def __str__(self):
        return self._to_dot()

    def _to_dot(self, assubgraph = False, digraph = None, newname = None, extraprefix = ""):
        """
        Internal method that calls :meth:`_to_dot` of subgraphs.
        """
        prefix = extraprefix+self.prefix
        if assubgraph:
            if self.cluster:
                dot = "subgraph cluster_"+prefix+newname+" {\n"
            else:
                dot = "subgraph "+prefix+newname+" {\n"
        else:
            digraph = self.digraph
            if self.strict:
                dot = "strict "
            else:
                dot = ""
            if digraph:
                dot += "digraph "+self.name+" {\n"
            else:
                dot += "graph "+self.name+" {\n"

        for i in xrange(len(self.keys())):
            key = self.keys()[i]
            #nodes are a string
            #edges are tuples of length two (from, to)
            #subgraphs are a string
            try:
                ""+key
            except TypeError:
                #it must be an edge
                assert len(key) == 2
                if digraph:
                    dot += "\t"+prefix+key[0]+" -> "+prefix+key[1]
                else:
                    dot += "\t"+prefix+key[0]+" -- "+prefix+key[1]

                attribs = self.content[i]
                dot += " ["
                for attrib in attribs:
                    try:
                        ""+attribs[attrib]
                    except TypeError:
                        #it is not a string attribute
                        #assume it is correct of we convert it to one
                        dot += str(attrib)+"="+str(attribs[attrib])+", "
                    else:
                        #it is a string attribute
                        if '"' not in attribs[attrib]:
                            dot += str(attrib)+'="'+str(attribs[attrib])+'", '
                        else:
                            # " is in the string
                            #therefore we assume it is properly formatted and add it directly
                            dot += str(attrib)+"="+str(attribs[attrib])+", "
                if len(attribs) > 0:
                    #trim off the last two characters ', '
                    dot = dot[:-2]
                dot += "]"
                dot += ";\n"

            else:
                #could be a node or a subgraph
                if self[key].__class__ == self.__class__:
                    #it is a subgraph
                    #ensure edge directionness and name are passed
                    subgstr = self[key]._to_dot(True, digraph, key, prefix)
                    #indent it correctly
                    subgstr = subgstr.replace("\n\t", "\n\t\t")
                    dot += "\t"+subgstr
                else:
                    #it is a node
                    #nodes are a string
                    
                    #dont prefix special nodes
                    if key in ("node", "edge", "graph", "subgraph"):
                        dot += "\t"+key
                    else:
                        dot += "\t"+prefix+key

                    attribs = self[key]
                    dot += " ["
                    for attrib in attribs:
                        try:
                            ""+attribs[attrib]
                        except TypeError:
                            #it is not a string attribute
                            #assume it is correct of we convert it to one
                            dot += str(attrib)+"="+str(attribs[attrib])+", "
                        else:
                            #it is a string attribute
                            if '"' not in attribs[attrib]:
                                dot += str(attrib)+'="'+str(attribs[attrib])+'", '
                            else:
                                # " is in the string
                                #therefore we assume it is properly formatted and add it directly
                                dot += str(attrib)+"="+str(attribs[attrib])+", "
                    if len(attribs) > 0:
                        #trim off the last two characters ', '
                        dot = dot[:-2]
                    dot += "]"
                    dot += ";\n"


        dot += "}"
        if assubgraph:
            dot += "\n"
        return dot

    def plot(self, output='pdf', prog='dot', args=()):
        """
        Calls the specified drawing program to turn this into an image.
        
        Use args to pass extra arguments, particularly ``-o`` to specify an output filename.
        
        Follows the same format as subprocess calls.
        """
        newargs = (prog, '-T'+output)+tuple(args)
        run = subprocess.Popen(newargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return run.communicate(self._to_dot())[0]

    #todo: put dictionary-like interface
    #e.g. foo["n1"]["style"] = "filled"
