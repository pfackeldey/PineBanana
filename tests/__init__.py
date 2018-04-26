# -*- coding: utf-8 -*-

__all__ = ["TestCase"]

import os
import sys
import unittest

base = os.path.normpath(os.path.join(os.path.abspath(__file__), "../.."))
sys.path.append(base)
from tools import *


class TestCase(unittest.TestCase):
    """
    Unittests... add more tests here!
    """

    def test_flattenlist(self):
        a = [[1., 2.], [3.]]
        self.assertEqual(flattenList(a), [1., 2., 3.])
