import io
import os.path
import sys
from load_data import main


class TestE2EIntegration:
    config_path = os.path.join(os.path.pardir, 'config.json')

    def test_empty_string_input(self):
        out = io.StringIO()
        sys.stdout = out
        main(['load_data.py', '--config', TestE2EIntegration.config_path])
        sys.stdout = sys.__stdout__
        assert out.getvalue().strip().startswith('Expected at least one argument')

    def test_incorrect_string_input(self):
        out = io.StringIO()
        sys.stdout = out
        main(['load_data.py', 'ABC', '--config', TestE2EIntegration.config_path])
        sys.stdout = sys.__stdout__
        assert out.getvalue().strip() == 'argument "ABC" was ignored'

    def test_correct_string_input(self):
        out = io.StringIO()
        sys.stdout = out
        main(['load_data.py', 'STI', '--config', TestE2EIntegration.config_path])
        sys.stdout = sys.__stdout__
        assert out.getvalue().strip() == 'Compound(STI)'

    def test_correct_string_multi_input(self):
        out = io.StringIO()
        sys.stdout = out
        main(['load_data.py', 'DPM', 'STI', '--config', TestE2EIntegration.config_path])
        sys.stdout = sys.__stdout__
        assert 'Compound(DPM)' in out.getvalue().strip()
        assert 'Compound(STI)' in out.getvalue().strip()

    def test_string_multi_input(self):
        out = io.StringIO()
        sys.stdout = out
        main(['load_data.py', 'ABC', 'STI', '--config', TestE2EIntegration.config_path])
        sys.stdout = sys.__stdout__
        assert 'argument "ABC" was ignored' in out.getvalue().strip()
        assert 'Compound(STI)' in out.getvalue().strip()
