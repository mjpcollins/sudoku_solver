import unittest
from tests.unittests import *


class TestSuiteLoader:

    def __init__(self):
        self.test_loader = unittest.TestLoader()
        self.test_suite = unittest.TestSuite()
        self.all_tests = list()
        self.load_tests()

    def load_tests(self):
        self._add_tests()
        self._add_all_tests_to_test_suite()

    def _add_tests(self):
        self._add_test_to_list_of_tests(TestVertex)
        self._add_test_to_list_of_tests(TestGraph)
        self._add_test_to_list_of_tests(TestSudokuPuzzle)
        self._add_test_to_list_of_tests(TestSolver)

    def _add_test_to_list_of_tests(self, test_object):
        self.all_tests.append(self.test_loader.loadTestsFromTestCase(test_object))

    def _add_all_tests_to_test_suite(self):
        for test_loader_class in self.all_tests:
            self.test_suite.addTest(test_loader_class)
