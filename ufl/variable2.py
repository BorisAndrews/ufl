"""Defines symbol and variable constructs."""

__authors__ = "Martin Sandve Alnes"
__date__ = "2008-05-20 -- 2009-01-09"

from ufl.common import Counted
from ufl.output import ufl_assert
from ufl.expr import Expr
from ufl.terminal import Terminal

class Label(Terminal, Counted):
    _globalcount = 0
    __slots__ = ()
    def __init__(self, count=None):
        Counted.__init__(self, count)
    
    def __str__(self):
        return "Label(%d)" % self._count
    
    def __repr__(self):
        return "Label(%d)" % self._count
    
    def __hash__(self):
        return hash(repr(self))

class NewVariable(Expr):
    """A NewVariable is a representative for another expression.
    
    It will be used by the end-user mainly for:
    - Defining a quantity to differentiate w.r.t. using diff.
    
    Internally, it is also used for:
    - Marking good spots to split an expression for optimized computation.
    - Reuse of expressions during e.g. automatic differentation.
    """
    __slots__ = ("_expression", "_label")
    def __init__(self, expression, label=None):
        Expr.__init__(self)
        
        ufl_assert(isinstance(expression, Expr), "Expecting an Expr.")
        self._expression = expression
        
        if label is None:
            label = Label()
        ufl_assert(isinstance(label, Label), "Expecting a Label.")
        self._label = label
    
    def operands(self):
        return (self._expression, self._label)
    
    def free_indices(self):
        return self._expression.free_indices()
    
    def index_dimensions(self):
        return self._expression.index_dimensions()
    
    def shape(self):
        return self._expression.shape()
    
    def cell(self):
        return self._expression.cell()
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self._label._count == other._label._count
        
    def __str__(self):
        return "Variable(%s, %s)" % (self._expression, self._label)
    
    def __repr__(self):
        return "Variable(%r, %r)" % (self._expression, self._label)

