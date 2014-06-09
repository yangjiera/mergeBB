def get_gt():
    gt = dict([])
    for line in open('groud_truth.csv'):
        fields = line.split(';')
        id = fields[0]
        amount = fields[3]
        prominence = fields[4]
        nrflowers_lower = fields[10]
        nrflowers_upper = fields[11]
        nrtypes_lower = fields[12]
        nrtypes_upper = fields[13]
        gt[id] = [amount, prominence, nrflowers_lower, nrflowers_upper, nrtypes_lower, nrtypes_upper]
        
    return gt
    
if __name__ == '__main__':
    get_gt()