#!/usr/bin/env python3
import logging
import argparse
import os
import stat
from datetime import datetime

logger = logging.getLogger("jove")


class Analysis:
    DIRNAME_DATA = "data"
    DIRNAME_FIGURES = "figures"
    FILENAME_README = "README.md"
    FILENAME_CODE = "code.py"
    FILENAME_WIP = "wip.py"
    FILENAME_LIB = "libjove.py"
    FILENAME_SHELL = "shell.sh"

    def __init__(self, chroot: str, name: str, **kwargs):
        self.chroot = chroot or os.getcwd()
        self.name = name

    @property
    def analysisdir(self):
        return os.path.join(self.chroot, self.name)

    @property
    def datadir(self):
        return os.path.join(self.analysisdir, self.DIRNAME_DATA)

    @property
    def figuresdir(self):
        return os.path.join(self.analysisdir, self.DIRNAME_FIGURES)

    def add_template(self, templatename, executable=False, overwrite=False, **kwargs):
        pathname = os.path.join(self.analysisdir, templatename)
        if not overwrite and os.path.exists(pathname):
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
        self.add_template(self.FILENAME_README, name=self.name)
        self.add_template(
            self.FILENAME_LIB,
            dirname_data=self.DIRNAME_DATA,
            dirname_figures=self.DIRNAME_FIGURES,
        )
        self.add_template(self.FILENAME_CODE)
        self.add_template(self.FILENAME_WIP)
        self.add_template(self.FILENAME_SHELL, executable=True)
        return self

    def upgrade(self):
        self.add_template(
            self.FILENAME_LIB,
            overwrite=True,
            dirname_data=self.DIRNAME_DATA,
            dirname_figures=self.DIRNAME_FIGURES,
        )
        self.add_template(self.FILENAME_SHELL, overwrite=True, executable=True)
        return self


def with_zettel_prefix(name):
    return datetime.now().strftime("%Y%m%d%H%M") + " - " + name


def startanalysis(name, chroot=None, zettel=False):
    if zettel:
        name = with_zettel_prefix(name)
    return Analysis(chroot=chroot, name=name, zettel=zettel).create()


def upgradeanalyses(dirnames):
    for dirname in dirnames:
        analysis = Analysis(
            chroot=os.path.dirname(dirname),
            name=os.path.basename(dirname),
        )
        analysis.upgrade()
        logger.info("Upgraded %s", dirname)


def _add_parser_start(subparsers):
    parser = subparsers.add_parser(
        "start", help="Initializes all analysis files in a new directory"
    )
    parser.add_argument(
        "name",
        help="Directory name for the analysis",
    )
    parser.add_argument(
        "-C",
        "--directory",
        help="Parent directory (defaults to current working directory)",
    )
    parser.add_argument(
        "-z",
        "--zettel",
        action="store_true",
        help="Prefix the analysis directory with a Zettlekasten-style timestamp",
    )


def _add_parser_upgrade(subparsers):
    parser = subparsers.add_parser(
        "upgrade",
        help="Upgrades framework files in analyses (note: doesn't touch user code)",
    )
    parser.add_argument("directory", nargs="+")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_parser_start(subparsers)
    _add_parser_upgrade(subparsers)
    args = parser.parse_args()
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    if args.command == "start":
        startanalysis(args.name, chroot=args.directory, zettel=args.zettel)
    elif args.command == "upgrade":
        upgradeanalyses(args.directory)
    else:
        raise ValueError(args.command)


if __name__ == "__main__":
    main()
