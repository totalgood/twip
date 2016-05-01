"""Run doctests in twip.util"""

import doctest

import twip.util

from django.test import TestCase


class T(TestCase):
    """Do-Nothing Test to ensure unittest doesnt ignore this file"""

    def setUp(self):
        pass

    def test_truth(self):
        self.assertTrue(True)


def load_tests(loader, tests, ignore):
    """Run doctests for the clayton.nlp module"""
    tests.addTests(doctest.DocTestSuite(twip.util, optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE))
    return tests
