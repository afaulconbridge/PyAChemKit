"""
Various functions that interact with NetworkX (http://networkx.lanl.gov/)

"""
import re
import itertools

import networkx

import reactionnet

def ReactionNetwork_to_MultiDiGraph(net):
    """
    Converts a ReactionNetwork (or class with same interface) to a MultiDiGraph.
    
    Converts each reaction into a node, and each molecular species into a node.
    """
    G = networkx.MultiDiGraph()
    
    for mol in net.seen:
        G.add_node(mol)
    for i in xrange(len(net.reactions)):
        r = "R%d"%i
        reaction = net.reactions[i]
        reactants, products = reaction
        
        reactstring = reactionnet.ReactionNetwork.reaction_to_string(reaction, net.rates[reaction])
        G.add_node(r, rate=net.rates[reaction], reaction = reactstring)
        for mol in reactants:
            G.add_edge(mol, r)
        for mol in products:
            G.add_edge(r, mol)
        
    return G
    
def MultiDiGraph_make_flow(G, sizeprop = 0.5, catalysts = True):
    """
    Creates a `flow` network from a MultiDiGraph (usually created by ReactionNetwork_to_MultiDiGraph).
    
    `sizeprop` is the proportion if the larger molecule that must be contained in the smaller one.
    
    `catalysts` determines if catalsysts should be considered when looking at edges between reactants and products.
    If this is false, then molecules that are both in the reactants and the products are removed and do not flow.
    """
    
    F = networkx.DiGraph()
    for node in G.nodes():
        if re.match(r"^R[0-9]+$",node) != None:
            #this is a reaction node
            reactants = tuple(sorted(list(set( ( e[0] for e in G.in_edges([node]) ) ))))
            products = tuple(sorted(list(set( ( e[1] for e in G.out_edges([node]) ) ))))
            reaction = G.node[node]["reaction"]
            
            #F.add_nodes_from(reactants)
            #F.add_nodes_from(products)
            
            for reactant, product in itertools.product(reactants, products):
                #no self-loops
                if reactant == product:
                    continue
                if catalysts is False:
                    if reactant in products or product in reactants:
                        continue
                    
                #print reactant, product
                nreactant = re.sub(r"[0-9\[\]]", "", reactant)
                nproduct = re.sub(r"[0-9\[\]]", "", product)
                #print reactant, product
                
                if len(nproduct) < len(nreactant):
                    small = nproduct
                    big = nreactant
                else:
                    small = nreactant
                    big = nproduct
                    
                if float(len(small)) / float(len(big)) > sizeprop and small in big:
                    F.add_node(reactant)
                    F.add_node(product)
                    F.add_edge(reactant, product, reaction=reaction)

    return F
    
def find_cycles(G):
    """
    Find some of the cycles in G. 
    
    Does this by splitting it into strongly connected subgraphs, then for each edge of each node
    find the shorted path exists that goes the other way. If it does, then it is a cycle.
    
    Once cycles are found, they are ordered so the lowest node is first. Repeated cycles are ignored.
    
    Ineffeicient algorithm, needs optimization for large highly-connected graphs.
    """    
    
    cycles = set()
    for g in networkx.strongly_connected_component_subgraphs(G):
        if len(g) > 1:
            #print g, len(g)
            for a in g:
                neighbours = []
                for edge in g.edges():
                    #print edge
                    if edge[0] == a:
                        neighbours.append(edge[1])
                for other in neighbours:
                    #this only gets one shortest path, not all possible paths
                    path = networkx.networkx.shortest_path(g, other, a)
                    #will always be there because its a stongly connected component
                    start = min(path)
                    sid = path.index(start)
                    cycle = path[sid:]+path[:sid]
                    #print start, other, path, cycle
                    cycles.add(tuple(cycle))
            
    cycles = tuple(sorted(list(cycles)))
    return cycles
