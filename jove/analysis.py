#!/usr/bin/env python3
import logging
import argparse
import os
import stat
from datetime import datetime

logger = logging.getLogger("jove")


class Analysis:
    DIRNAME_ANALYSIS_DATA = "data"
    DIRNAME_ANALYSIS_FIGURES = "figures"
    FILENAME_ANALYSIS_README = "README.md"
    FILENAME_ANALYSIS_CODE = "code.py"
    FILENAME_ANALYSIS_LIB = "lib.py"
    FILENAME_ANALYSIS_SHELL = "shell.sh"

    def __init__(self, projectdir: str, name: str, **kwargs):
        self.projectdir = projectdir or os.getcwd()
        self.name = name

    @property
    def analysisdir(self):
        return os.path.join(self.projectdir, self.name)

    @property
    def datadir(self):
        return os.path.join(self.analysisdir, self.DIRNAME_ANALYSIS_DATA)

    @property
    def figuresdir(self):
        return os.path.join(self.analysisdir, self.DIRNAME_ANALYSIS_FIGURES)

    def add_template(self, templatename, executable=False, **kwargs):
        pathname = os.path.join(self.analysisdir, templatename)
        if os.path.exists(pathname):
            raise Exception(f"{pathname} already exists")
        with open(
            os.path.join(os.path.dirname(__file__), "templates", templatename)
        ) as t, open(pathname, "w") as o:
            template = t.read().format(**kwargs)
            o.write(template)
        if executable:
            st = os.stat(pathname)
            os.chmod(pathname, st.st_mode | stat.S_IEXEC)
        logger.info("Created %s", pathname)

    def add_dir(self, dirname):
        os.makedirs(dirname, exist_ok=False)
        logger.info("Created %s", dirname)

    def create(self):
        self.add_dir(self.analysisdir)
        self.add_dir(self.datadir)
        self.add_dir(self.figuresdir)
        self.add_template(self.FILENAME_ANALYSIS_README, name=self.name)
        self.add_template(
            self.FILENAME_ANALYSIS_LIB,
            dirname_data=self.DIRNAME_ANALYSIS_DATA,
            dirname_figures=self.DIRNAME_ANALYSIS_FIGURES,
        )
        self.add_template(self.FILENAME_ANALYSIS_CODE)
        self.add_template(self.FILENAME_ANALYSIS_SHELL, executable=True)
        return self


def with_zettel_prefix(name):
    return datetime.now().strftime("%Y%m%d%H%M") + " - " + name


def startanalysis(name, projectdir=None, zettel=False):
    if zettel:
        name = with_zettel_prefix(name)
    return Analysis(projectdir=projectdir, name=name, zettel=zettel).create()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_start = subparsers.add_parser("start")
    parser_start.add_argument("name", help="Directory name for the analysis")
    parser_start.add_argument(
        "--projectdir", help="Parent directory (defaults to current working directory)"
    )
    parser_start.add_argument("--zettel", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    if args.command == "start":
        startanalysis(args.name, projectdir=args.projectdir, zettel=args.zettel)
    else:
        raise ValueError(args.command)


if __name__ == "__main__":
    main()
