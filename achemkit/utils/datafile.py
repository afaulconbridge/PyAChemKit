


def data_to_lines(data):
    #calculate headings
    headings = set()
    for y in data:
        headings.update(data[y].keys())
    headings = sorted(headings)
    
    #output header
    line = "\t"+"\t".join(str(x) for x in headings)+"\n"
    yield line
    
    #output data
    for y in sorted(data.keys()):
        line = "{0}\t".format(y)
        for x in headings:
            if x in data[y]:
                line += "{0}".format(data[y][x])
            else:
                line += "{0}".format(None)
            if x is not headings[-1]:
                line += "\t"
        line += "\n"
        yield line
        
def data_to_file(data, outfile):
    for line in data_to_lines(data):
        outfile.write(line)
        
def data_from_lines(lines):
    data = {}
    headings = None
    for line in lines:
        if headings is None:
            headings = line.strip().split("\t")
        else:
            row = line.split() #dont strip, end may be blank
            y = row[0]
            assert y not in data
            data[y] = {}
            assert len(row) >= len(headings)+1
            for i in xrange(1, len(headings)):
                data[y][headings[i-1]] = row[i]
    return data
    
def data_from_file(infile):
    return data_from_lines(infile.readlines())
