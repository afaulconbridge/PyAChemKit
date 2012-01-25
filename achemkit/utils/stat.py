

def mean(values):
    return sum(values) / float(len(values))
    
def median(values):
    return sorted(values)[len(values) // 2]
    
def quartile_upper(values):
    return sorted(values, reverse=True)[len(values) // 4]
    
def quartile_lower(values):
    return sorted(values)[len(values) // 4]
    
def standard_deviation(values):
    raise NotImplementedError
    
def standard_error(values):
    raise NotImplementedError    
    
def correlation(values1, values2):
    raise NotImplementedError
