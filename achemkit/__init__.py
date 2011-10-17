"""
Detailed documentation for all the components of AChemKit.
It is generated directly from the source code, so should be up-to-date.
"""

# Import Psyco if available
try:
    import psyco
    psyco.full()
except ImportError:
    pass
   
__version__ = "0.4.0"
   
from achemkit.reactionnet import ReactionNetwork
from achemkit.reactionnetdot import net_to_dot 
from achemkit.utils.simpledot import SimpleDot
from achemkit.randomnet import Uniform
from achemkit.randomnet import Linear
from achemkit.utils.bag import Bag, FrozenBag, OrderedBag, OrderedFrozenBag
from achemkit.bucket import Bucket, Event
from achemkit.achem import AChem, AChemReactionNetwork
from achemkit.sim.simple import sim_enumerate, sim_itterative, sim_stepwise
from achemkit.sim.simple import ReactorEnumerate, ReactorItterative, ReactorStepwise
from achemkit.sim.gillespie import simulate_gillespie as sim_gillespie

