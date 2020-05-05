# -*- coding: utf-8 -*-
"""This module contains the apply_transforms algorithm which propagates transform operators in a form towards the terminals."""

# Copyright (C) 2008-2016 Martin Sandve Alnæs
#
# This file is part of UFL (https://www.fenicsproject.org)
#
# SPDX-License-Identifier:    LGPL-3.0-or-later


from ufl.log import error
from ufl.classes import FormArgument, Transformed
from ufl.corealg.multifunction import MultiFunction
from ufl.corealg.map_dag import map_expr_dag
from ufl.algorithms.map_integrands import map_integrand_dags
from ufl.measure import integral_type_to_measure_name


class TransformedRuleset(MultiFunction):
    def __init__(self, transform_op):
        MultiFunction.__init__(self)
        self._transform_op = transform_op

    def terminal(self, o):
        return o

    expr = MultiFunction.reuse_if_untouched

    def reference_value(self, o):
        "Must act directly on reference value of argument objects."
        f, = o.ufl_operands
        assert f._ufl_is_terminal_
        assert isinstance(f, FormArgument)
        return Transformed(o, self._transform_op)


class TransformedRuleDispatcher(MultiFunction):
    def __init__(self):
        MultiFunction.__init__(self)

    def terminal(self, o):
        return o

    expr = MultiFunction.reuse_if_untouched

    def transformed(self, o, A, transform_op):
        rules = TransformedRuleset(transform_op)
        return map_expr_dag(rules, A)


def apply_transforms(expression):
    "Propagate filter nodes to wrap reference value argument directly."
    rules = TransformedRuleDispatcher()
    return map_integrand_dags(rules, expression)
