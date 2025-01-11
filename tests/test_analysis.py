import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import patch
from jove.analysis import startanalysis, with_zettel_prefix


class TestAnalysis:
    NAME = "myanalysis"

    @pytest.fixture(scope="class")
    def root(self):
        with tempfile.TemporaryDirectory() as tmp:
            startanalysis(self.NAME, chroot=tmp)
            root = os.path.join(tmp, self.NAME)
            assert os.path.exists(root)
            yield root

    def test_files_exist(self, root):
        for dirname in ["data", "figures"]:
            pathname = os.path.join(root, dirname)
            assert os.path.exists(pathname)
            assert os.path.isdir(pathname)
        for filename in ["shell.sh", "code.py", "libjove.py", "wip.py", "README.md"]:
            pathname = os.path.join(root, filename)
            assert os.path.exists(pathname)
            assert os.path.isfile(pathname)

    def test_readme_title(self, root):
        with open(os.path.join(root, "README.md")) as f:
            header = f.read().splitlines()[0]
            assert "myanalysis" in header

    def test_lib_directories(self, root):
        found_data = False
        found_figures = False
        with open(os.path.join(root, "libjove.py")) as f:
            for line in f:
                line = line.strip()
                if line == 'DIRNAME_DATA = "data"':
                    found_data = True
                if line == 'DIRNAME_FIGURES = "figures"':
                    found_figures = True
        assert found_data
        assert found_figures

    def test_shell_executable(self, root):
        shellfile = os.path.join(root, "shell.sh")
        assert os.path.isfile(shellfile) and os.access(shellfile, os.X_OK)

    def test_shell_codefiles(self, root):
        shellfile = os.path.join(root, "shell.sh")
        with open(shellfile) as f:
            content = f.read()
            assert "libjove.py code.py wip.py" in content


def test_with_zettel_prefix():
    fixed_time = datetime(2025, 1, 1)
    with patch("jove.analysis.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        name = with_zettel_prefix("My Analysis")
        assert name == "202501010000 - My Analysis"
