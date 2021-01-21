from copy import deepcopy
import sympy as sym

class MySymbol(object):

    def __init__(self, symbol):
        
        self.var = symbol
        self.coeff = 1
        self.pow = 1
        
    def __repr__(self):
        
        sym = self.var
        
        if self.coeff == 0:
            return '0'
        
        elif self.coeff == -1:
            sym = f'-{sym}'
            
        elif self.coeff != 1:
            sym = f'{self.coeff}{sym}'
        
        
        if self.pow == 0:
            return '1'
        
        elif self.pow != 1:
            sym += f'^{self.pow}'
            
        return sym
    
    def _repr_html_(self):
        
            
        return f"${self}$"
    
    
    def copy(self):
        
        return deepcopy(self)
    
    
    def __pos__(self):
        return self.copy()
    
    def __neg__(self):
        
        res = self.copy()
        
        res.coeff = -res.coeff
        
        return res
        
    def __add__(self, other):
        
        res = self.copy()
        
        if type(other) == type(res):
            
            if (other.var==res.var) and (other.pow == res.pow):
                
                res.coeff += other.coeff
                
                return res
        
#         return res
    
    def __sub__(self, other):
        
        return self + (-other)
        
    
    def __rsub__(self, other):
        
        return other + (-self)
    
    def __radd__(self, other):
        
        # commutative
        return self.__add__(other)
    

class MyExpr(object):
    
    def __init__(self, terms):
        
        self.terms = terms
        
    def __repr__(self):
        
        res = ''
        
        for t in terms:
            res += str()
            
            
class Algebra(object):
    
    def __init__(self, x):
        
        self._sym = str(x)
        self._pow = 1
        self._coef = 1
        self._neg = False
        
    @property
    def symbol(self):
        
        s = self._sym

        if str(self._pow) != '1' and str(self._sym) != '1':
            s += '^{' + str(self._pow) + '}'
            
        if str(self._coef) != '1':
            s = str(self._coef) + s
            
        if self._neg:
            s = '-' + s
            
        return s
    
    def copy(self):
        
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        
        return result
    
    def _repr_html_(self):
        
        s = r"$\displaystyle %s$" % self.symbol.strip('$')
        return s
        
    def __repr__(self):
        
        return self.symbol
    
    def __neg__(self):
        
        res = self.copy()
        res._neg = not res._neg
        
        return res
    
    def __pos__(self):
        
        return self

    def __mul__(self, other):
        
        if str(other) == 1:
            return self
        
        elif str(other) == 0:
            return self.__init__('0')
            
        res = self.copy()
        
        if type(other) != type(res):
            res._coef *= other
        
        elif other._sym == res._sym:
            res._coef *= other._coef
            res._pow += other._pow
            
        return res
    
    def __rmul__(self, other):
        
        return self.__mul__(other)
        
    def __pow__(self, other):
        
        if str(other) == '0':
            return self.__init__('1')
            
        res = self.copy()
        res._pow = res._pow * other
        res._coef = res._coef ** other

        return res
    
    
class Compound:
    
    def __init__(self, *args):
        
        
n = Algebra('n')
m = Algebra('m')
2*m**2
