import sys
from unittest import TextTestRunner
from _tests.unittests_utils.unittest_loader import TestSuiteLoader


class AllTestsRunner(TestSuiteLoader):

    def __init__(self):
        super().__init__()
        self.tests_result = bool()

    def run_tests(self):
        runner = TextTestRunner()
        return runner.run(self.test_suite).wasSuccessful()


def run():
    if not AllTestsRunner().run_tests():
        sys.exit(1)


if __name__ == '__main__':
    run()
