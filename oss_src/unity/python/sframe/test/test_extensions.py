'''
Copyright (C) 2015 Dato, Inc.
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
'''
import unittest
from ..data_structures.sarray import SArray
from ..data_structures.sframe import SFrame
import random


class VariantCheckTest(unittest.TestCase):

    def identical(self, reference, b):
        if type(reference) in [int, long]:
            self.assertTrue(type(b) in [int, long])
        else:
            self.assertEquals(type(reference), type(b))
        if isinstance(reference, list):
            self.assertEquals(len(reference), len(b))
            for i in range(len(reference)):
                self.identical(reference[i], b[i])
        if isinstance(reference, dict):
            self.assertEqual(sorted(reference.iterkeys()), sorted(b.iterkeys()))
            for i in reference:
                self.identical(reference[i], b[i])
        if isinstance(reference, SArray):
            self.identical(list(reference), list(b))
        if isinstance(reference, SFrame):
            self.identical(list(reference), list(b))

    def variant_turnaround(self, reference, expected_result=None):
        if expected_result is None:
            expected_result = reference
        from ..extensions import _demo_identity
        self.identical(expected_result, _demo_identity(reference))

    def test_variant_check(self):
        sa = SArray([1,2,3,4,5])
        sf = SFrame({'a':sa})
        import array
        self.variant_turnaround(1)
        self.variant_turnaround(1.0)
        self.variant_turnaround(array.array('d', [1.0, 2.0, 3.0]))
         # numeric lists currently converts to array
        self.variant_turnaround([1, 2, 3], array.array('d',[1,.0,2.0,3.0]))
        self.variant_turnaround("abc")
        self.variant_turnaround(["abc", "def"])
        self.variant_turnaround({'a':1,'b':'c'})
        self.variant_turnaround({'a':[1,2,'d'],'b':['a','b','c']})
         # numeric lists currently converts to array
        self.variant_turnaround({'a':[1,2,3],'b':['a','b','c']},
                                {'a':array.array('d',[1,2,3]),'b':['a','b','c']})
        self.variant_turnaround(sa)
        self.variant_turnaround(sf)
        self.variant_turnaround([sa,sf])
        self.variant_turnaround([sa,sa])
        self.variant_turnaround([sf,sf])
        self.variant_turnaround({'a':sa, 'b':sf, 'c':['a','b','c','d']})
        self.variant_turnaround({'a':[sa,sf,{'a':sa,'b':'c'}],
            'b':sf, 'c':['a','b','c','d']})

        
    def test_stress(self):

        random.seed(0)

        def _make(depth):

            if depth == 0:
                s = random.randint(0, 3)
            else:
                s = random.randint(0, 5)

            if s == 0:
                return str(random.randint(0, 100))
            elif s == 1:
                return random.randint(0,100000)
            elif s == 2:
                return SArray([random.randint(0,100000) for i in range(2)])
            elif s == 3:
                return SFrame({'a' : [random.randint(0,100000) for i in range(2)],
                               'b' : [str(random.randint(0,100000)) for i in range(2)]})

            elif s == 4:
                length = random.randint(3, 8)
                # The ['a'] needed so it doesn't get translated to a string.
                return ['a'] + [_make(depth - 1) for i in range(length)]
            elif s == 5:
                length = random.randint(3, 8)
                return {str(random.randint(0, 100)) : _make(depth - 1)
                        for i in range(length)}

        for i in range(10):
            self.variant_turnaround(_make(5 + i))
