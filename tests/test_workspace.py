import tempfile
import os
import json
from jove.workspace import newproject, newanalysis
from datetime import datetime


def test_workspace():
    with tempfile.TemporaryDirectory() as tmp:
        # Create new project
        newproject(tmp)
        configfile = os.path.join(tmp, ".jove.json")
        assert os.path.exists(configfile)
        with open(configfile) as f:
            config = json.load(f)
            assert config["zettel"] == False
            assert config["created_at"] is not None
        # Add an analysis to the project
        newanalysis("myanalysis", projectdir=tmp)
        analysisdir = os.path.join(tmp, "myanalysis")
        assert os.path.exists(analysisdir)
        for dirname in ["data", "figures"]:
            pathname = os.path.join(analysisdir, dirname)
            assert os.path.exists(pathname)
            assert os.path.isdir(pathname)
        for filename in ["shell.sh", "code.py", "lib.py", "README.md"]:
            pathname = os.path.join(analysisdir, filename)
            assert os.path.exists(pathname)
            assert os.path.isfile(pathname)
        # Title of README
        with open(os.path.join(analysisdir, "README.md")) as f:
            header = f.read().splitlines()[0]
            assert "myanalysis" in header
        # Data / figure directories
        found_data = False
        found_figures = False
        with open(os.path.join(analysisdir, "lib.py")) as f:
            for line in f:
                line = line.strip()
                if line == 'DIRNAME_DATA = "data"':
                    found_data = True
                if line == 'DIRNAME_FIGURES = "figures"':
                    found_figures = True
        assert found_data
        assert found_figures
        # shell.sh executable
        shellfile = os.path.join(analysisdir, "shell.sh")
        assert os.path.isfile(shellfile) and os.access(shellfile, os.X_OK)


def test_workspace_zettel():
    with tempfile.TemporaryDirectory() as tmp:
        # Create new project
        newproject(tmp, zettel=True)
        configfile = os.path.join(tmp, ".jove.json")
        assert os.path.exists(configfile)
        with open(configfile) as f:
            config = json.load(f)
            assert config["zettel"] == True
            assert config["created_at"] is not None
        # Add an analysis to the project
        newanalysis("My Great Analysis", projectdir=tmp)
        analysisdir = None
        for dirname in os.listdir(tmp):
            if "my-great-analysis" in dirname:
                analysisdir = dirname
                break
        assert analysisdir is not None
        ts = datetime.strptime(analysisdir.split("-")[0], "%Y%m%d%H%M")
        assert ts is not None
        analysisdir = os.path.join(tmp, analysisdir)
        assert os.path.exists(analysisdir)
        for dirname in ["data", "figures"]:
            pathname = os.path.join(analysisdir, dirname)
            assert os.path.exists(pathname)
            assert os.path.isdir(pathname)
        for filename in ["shell.sh", "code.py", "lib.py", "README.md"]:
            pathname = os.path.join(analysisdir, filename)
            assert os.path.exists(pathname)
            assert os.path.isfile(pathname)
        # Title of README
        with open(os.path.join(analysisdir, "README.md")) as f:
            header = f.read().splitlines()[0]
            ts = ts.strftime("%Y%m%d%H%M")
            assert f"{ts} - My Great Analysis" in header
        # Data / figure directories
        found_data = False
        found_figures = False
        with open(os.path.join(analysisdir, "lib.py")) as f:
            for line in f:
                line = line.strip()
                if line == 'DIRNAME_DATA = "data"':
                    found_data = True
                if line == 'DIRNAME_FIGURES = "figures"':
                    found_figures = True
        assert found_data
        assert found_figures
        # shell.sh executable
        shellfile = os.path.join(analysisdir, "shell.sh")
        assert os.path.isfile(shellfile) and os.access(shellfile, os.X_OK)

