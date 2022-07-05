import io
import os.path
import sys
from db_helper import Compound
from load_data import main


def main_for_test(*arg, **kwarg):
    try:
        out = io.StringIO()
        sys.stdout = out
        main(*arg, **kwarg)
        return out.getvalue().strip()
    finally:
        sys.stdout = sys.__stdout__


class TestE2EIntegration:

    def test_empty_string_input(self):
        res = main_for_test(['load_data.py'])

        assert res.startswith('Expected at least one argument')

    def test_incorrect_string_input(self):
        res = main_for_test(['load_data.py', 'ABC'])

        assert res.startswith(
            'argument "ABC" was ignored\nExpected at least one argument')

    def test_correct_string_input(self):
        res = main_for_test(['load_data.py', 'STI'])

        assert res == 'Compound(STI)'

    def test_correct_string_multi_input(self):
        res = main_for_test(['load_data.py', 'DPM', 'STI'])

        assert str(Compound(compound='DPM')) in res
        assert str(Compound(compound='STI')) in res

    def test_string_multi_input(self):
        res = main_for_test(['load_data.py', 'ABC', 'STI'])

        assert 'argument "ABC" was ignored' in res
        assert str(Compound(compound='STI')) in res
