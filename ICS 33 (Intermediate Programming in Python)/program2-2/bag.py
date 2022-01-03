# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, iterable=None):
        self.bag = defaultdict(int)
        if (iterable != None) and (len(iterable) > 0):
            for thing in iterable:
                self.bag[thing] += 1
                
    def __repr__(self):
        iterable = []
        if len(self.bag) > 0:
            for thing, num in self.bag.items():
                while num > 0:
                    iterable.append(thing)
                    num -= 1
        return f'Bag({iterable})' if (len(iterable) > 0) else 'Bag()'
    
    def __str__(self):
        return 'Bag(' + ','.join(f'{thing}[{num}]' for thing, num in self.bag.items()) + ')' if (len(self.bag) > 0) else 'Bag()'
    
    def __len__(self):
        return sum(list(self.bag.values())) if len(self.bag) > 0 else 0
    
    def unique(self):
        return len(self.bag)
    
    def __contains__(self, thing):
        return True if thing in self.bag else False
    
    def count(self, thing):
        return self.bag[thing] if thing in self.bag else 0
    
    def add(self, thing):
        self.bag[thing] += 1
    
    def __add__(self, other):
        if type_as_str(self) == type_as_str(other):
            bag1 = repr(self).strip('Bag([])').replace('\'', '').split(', ')
            bag2 = repr(other).strip('Bag([])').replace('\'', '').split(', ')
            return Bag(bag1 + bag2)
        else:
            raise TypeError('One or more operand(s) is not a Bag object')
        
    def remove(self, thing):
        if thing in self.bag:
            self.bag[thing] -= 1
            if self.bag[thing] == 0:
                del self.bag[thing]
        else:
            raise ValueError('Argument was not found in bag; it could not be removed')
    
    def __eq__(self, other):
        if type_as_str(self) == type_as_str(other):
            if sorted(repr(self).strip('Bag([])').replace('\'', '').split(', ')) == sorted(repr(other).strip('Bag([])').replace('\'', '').split(', ')):
                return True
            else:
                return False
        else:
            return False
    
    def __ne__(self, other):
        if type_as_str(self) == type_as_str(other):
            if sorted(repr(self).strip('Bag([])').replace('\'', '').split(', ')) != sorted(repr(other).strip('Bag([])').replace('\'', '').split(', ')):
                return True
            else:
                return False
        else:
            return True
    
    def __iter__(self):
        def gen(bag):
            for thing in bag:
                yield thing
        return gen(repr(self).strip('Bag([])').replace('\'', '').split(', '))


if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Bag before doing the bsc tests
    #Debugging problems with these tests is simpler

    b = Bag(['d','a','d','b','c','b','d'])
    print(repr(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))
    for i in b:
        print(i)

    b2 = Bag(['a','a','b','x','d'])
    print(repr(b2+b2))
    print(str(b2+b2))
    print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()
    
    import driver
    driver.default_file_name = 'bscp21S21.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
