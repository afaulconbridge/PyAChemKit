"""
Various small functions that can get combined together.
"""

import random

def get_sample(distribution, rng=None):
    if rng is None:
        rng = random.Random()
    if isinstance(distribution, int) or isinstance(distribution, float):
        return distribution
    elif isinstance(distribution, list) or isinstance(distribution, tuple):
        return (rng.sample(distribution, 1))[0]
    elif isinstance(distribution, dict):
        #assume its a value:proportion dict
        total = sum(distribution.values())
        target = rng.random()*total
        i = 0
        score = distribution.values()[i]
        hit = distribution.keys()[i]
        while score < target:
            i += 1
            score += distribution.values()[i]
            hit = distribution.keys()[i]
        return hit

