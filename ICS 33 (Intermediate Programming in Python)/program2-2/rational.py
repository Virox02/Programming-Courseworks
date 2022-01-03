# Submitter: kimmk10 (Kim, Min Kee)
# Partner  : vvijaywa (Vijaywargiya, Viraj)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from goody import irange, type_as_str
import math

class Rational:
    @staticmethod
    # Called as Rational._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    def _gcd(x : int, y : int) -> int:
        assert type(x) is int and type(y) is int and x >= 0 and y >= 0,\
          'Rational._gcd: x('+str(x)+') and y('+str(y)+') must be integers >= 0'
        while y != 0:
            x, y = y, x % y
        return x
    
    @staticmethod
    # Called as Rational._validate_arithmetic(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Rational or int is...
    # Rational._validate_arithmetic(right, {Rational,int},'+','Rational',type_as_str(right))
    def _validate_arithmetic(v : object, t : {type}, op : str, left_type : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+left_type+'\' and \''+right_type+'\'')        

    @staticmethod
    # Called as Rational._validate_relational(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v : object, t : {type}, op : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Rational() '+op+' '+right_type+'()') 
                   

    def __init__(self, num=0, denom=1):
        if type(num) != int:
            raise AssertionError(f'Rational.__init__ numerator is not int: {num}')
        elif (type(denom) != int) or denom == 0:
            raise AssertionError(f'Rational.__init__ denominator is not int != 0: {denom}')
        else:
            self.num = num // Rational._gcd(abs(num), abs(denom)) if denom > 0 else -num // Rational._gcd(abs(num), abs(denom))
            self.denom = abs(denom) // Rational._gcd(abs(num), abs(denom))
    
    def __str__(self):
        return f'{self.num}/{self.denom}'
    
    def __repr__(self):
        return f'Rational({self.num},{self.denom})'
    
    def __bool__(self):
        return False if self.num == 0 else True
    
    def __getitem__(self, index):
        if index == 0 or index == 1:
            return self.num if index == 0 else self.denom
        elif type(index) == str and index != '' and ('numerator'.startswith(index.lower()) or 'denominator'.startswith(index.lower())):
            return self.num if 'numerator'.startswith(index.lower()) else self.denom
        else:
            raise TypeError(f'Invalid index: {index}')
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return Rational(-self.num, self.denom)
    
    def __abs__(self):
        return Rational(abs(self.num), self.denom)
    
    def __add__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'+','Rational',type_as_str(other))
        return Rational(self.num + (other * self.denom),self.denom) if type_as_str(other) == 'int' else Rational((self.num * other.denom) + (other.num * self.denom),self.denom * other.denom)
    
    def __radd__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'+','Rational',type_as_str(other))
        return Rational(self.num + (other * self.denom),self.denom) if type_as_str(other) == 'int' else Rational((self.num * other.denom) + (other.num * self.denom),self.denom * other.denom)
    
    def __sub__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'-','Rational',type_as_str(other))
        return Rational(self.num - (other * self.denom),self.denom) if type_as_str(other) == 'int' else Rational((self.num * other.denom) - (other.num * self.denom),self.denom * other.denom)
    
    def __rsub__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'-','Rational',type_as_str(other))
        return Rational((other * self.denom) - self.num,self.denom) if type_as_str(other) == 'int' else Rational((other.num * self.denom) - (self.num * other.denom),self.denom * other.denom)
    
    def __mul__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'*','Rational',type_as_str(other))
        return Rational(self.num * other,self.denom) if type_as_str(other) == 'int' else Rational(self.num * other.num,self.denom * other.denom)
    
    def __rmul__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'*','Rational',type_as_str(other))
        return Rational(self.num * other,self.denom) if type_as_str(other) == 'int' else Rational(self.num * other.num,self.denom * other.denom)
    
    def __truediv__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'/','Rational',type_as_str(other))
        return Rational(self.num,self.denom * other) if type_as_str(other) == 'int' else Rational(self.num * other.denom,self.denom * other.num)
    
    def __rtruediv__(self, other):
        Rational._validate_arithmetic(other, {Rational,int},'/','Rational',type_as_str(other))
        return Rational(other * self.denom,self.num) if type_as_str(other) == 'int' else Rational(other.num * self.denom,other.denom * self.num)
    
    def __pow__(self, exp):
        if type_as_str(exp) == 'int':
            return Rational(self.num ** exp, self.denom ** exp) if exp >= 0 else Rational(self.denom ** -exp, self.num ** -exp)
        else:
            raise TypeError(f'Power must be an int: {exp}')
    
    def __eq__(self, other):
        Rational._validate_relational(other, {Rational,int},'==',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return True if (self.num == other.num) and (self.denom == other.denom) else False
        else:
            return True if (self.num == other.num) and (self.denom == other.denom) else False
    
    def __ne__(self, other):
        Rational._validate_relational(other, {Rational,int},'!=',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return False if (self.num == other.num) and (self.denom == other.denom) else True
        else:
            return False if (self.num == other.num) and (self.denom == other.denom) else True
    
    def __lt__(self, other):
        Rational._validate_relational(other, {Rational,int},'<',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return True if (self.num < other.num * self.denom) else False
        else:
            return True if (self.num * other.denom < other.num * self.denom) else False
    
    def __gt__(self, other):
        Rational._validate_relational(other, {Rational,int},'>',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return True if (self.num > other.num * self.denom) else False
        else:
            return True if (self.num * other.denom > other.num * self.denom) else False
    
    def __le__(self, other):
        Rational._validate_relational(other, {Rational,int},'<=',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return True if (self.num <= other.num * self.denom) else False
        else:
            return True if (self.num * other.denom <= other.num * self.denom) else False
    
    def __ge__(self, other):
        Rational._validate_relational(other, {Rational,int},'>=',type_as_str(other))
        if type_as_str(other) == 'int':
            other = Rational(other,1)
            return True if (self.num >= other.num * self.denom) else False
        else:
            return True if (self.num * other.denom >= other.num * self.denom) else False
    
    def __call__(self, place):
        decimal = '' if self.num >= 0 else '-'
        decimal += f'{abs(self.num) // self.denom}.' if abs(self.num) // self.denom > 0 else '.'
        rem1 = abs(self.num) % self.denom
        while place > 0:
            quo, rem = divmod(rem1*(10), self.denom)
            decimal += f'{quo}'
            rem1 = rem
            place -= 1
        return decimal
            
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise NameError(f'{name} attribute cannot be changed to {value}')
        elif name == 'num' or name == 'denom':
            self.__dict__[name] = value
        else:
            raise NameError(f'{name} attribute cannot be added')
    
# e ~ 1/0! + 1/1! + 1/2! + 1/3! ... 1/n!
def compute_e(n):
    answer = Rational(1)
    for i in irange(1,n):
        answer += Rational(1,math.factorial(i))
    return answer

# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Rational(1,2)
    x      = Rational(1,2)
    for i in irange(1,n):
        big = 2*i+1
        answer += Rational(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer


if __name__ == '__main__':
    #Simple tests before running driver

    x = Rational(8,29)
    print(x)
    print(x+x)
    print(2*x)
    print(x(30))
    
    print()
    import driver    
    driver.default_file_name = 'bscp22S21.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
