class dotdict(dict):
# """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class unique_element:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    eset=set(elements)
    listunique = [unique_element(i,elements.count(i)) for i in eset]
    u=len(elements)
    return perm_unique_helper(listunique,[0]*u,u-1)

def perm_unique_helper(listunique,result_list,d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for g in  perm_unique_helper(listunique,result_list,d-1):
                    yield g
                i.occurrences+=1
                
def permute_unique(self, nums):
        perms = [[]]
        for n in nums:
            new_perm = []
            for perm in perms:
                for i in range(len(perm) + 1):
                    new_perm.append(perm[:i] + [n] + perm[i:])
                    # handle duplication
                    if i < len(perm) and perm[i] == n: break
            perms = new_perm
        return perms