#!/usr/bin/env python3
import logging
import argparse
import os
import json
import stat
import re
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger("jove")

DIRNAME_ANALYSIS_DATA = "data"
DIRNAME_ANALYSIS_FIGURES = "figures"
FILENAME_CONFIG = ".jove.json"
FILENAME_ANALYSIS_README = "README.md"
FILENAME_ANALYSIS_CODE = "code.py"
FILENAME_ANALYSIS_LIB = "lib.py"
FILENAME_ANALYSIS_SHELL = "shell.sh"


@dataclass
class Config:
    created_at: int = None
    updated_at: int = None
    zettel: bool = False

    @classmethod
    def read(cls, projectdir):
        if projectdir is None:
            projectdir = os.getcwd()
        with open(os.path.join(projectdir, FILENAME_CONFIG)) as f:
            return cls(**json.load(f))

    def write(self, projectdir):
        if projectdir is None:
            projectdir = os.getcwd()
        with open(os.path.join(projectdir, FILENAME_CONFIG), "w") as f:
            now = int(datetime.now().timestamp())
            if not self.created_at:
                self.created_at = now
            self.updated_at = now
            json.dump(self.__dict__, f)


class Project:
    def __init__(self, projectdir: str = None, config: Config = None, **kwargs):
        self.projectdir = projectdir or os.getcwd()
        self.config = config or Config()

    @property
    def configfile(self):
        return os.path.join(self.projectdir, FILENAME_CONFIG)

    def create(self):
        if os.path.exists(self.configfile):
            raise Exception(f"{self.projectdir} is already a project")
        os.makedirs(self.projectdir, exist_ok=True)
        self.config.write(self.projectdir)
        logger.info("Created %s", self.projectdir)
        return self


class Analysis:
    def __init__(self, project: Project, name: str, **kwargs):
        self.project = project
        self.name = name
        self.now = datetime.now().strftime("%Y%m%d%H%M")

    @property
    def analysisdir(self):
        slug = re.sub(r"\s+", "-", self.name.lower())
        if self.project.config.zettel:
            slug = "-".join([self.now, slug])
        return os.path.join(self.project.projectdir, slug)

    @property
    def datadir(self):
        return os.path.join(self.analysisdir, DIRNAME_ANALYSIS_DATA)

    @property
    def figdir(self):
        return os.path.join(self.analysisdir, DIRNAME_ANALYSIS_FIGURES)

    @property
    def title(self):
        return f"{self.now} - {self.name}" if self.project.config.zettel else self.name

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
        self.add_dir(self.figdir)
        self.add_template(FILENAME_ANALYSIS_README, title=self.title)
        self.add_template(
            FILENAME_ANALYSIS_LIB,
            dirname_data=DIRNAME_ANALYSIS_DATA,
            dirname_figures=DIRNAME_ANALYSIS_FIGURES,
        )
        self.add_template(FILENAME_ANALYSIS_CODE)
        self.add_template(FILENAME_ANALYSIS_SHELL, executable=True)
        return self


def newproject(projectdir, zettel=False):
    config = Config(zettel=zettel)
    return Project(projectdir=projectdir, config=config).create()


def newanalysis(name, projectdir=None):
    config = Config.read(projectdir)
    project = Project(projectdir=projectdir, config=config)
    return Analysis(project=project, name=name).create()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_newproject = subparsers.add_parser("newproject")
    parser_newproject.add_argument("projectdir", nargs="?")
    parser_newproject.add_argument("--zettel", action="store_true")
    parser_newanalysis = subparsers.add_parser("newanalysis")
    parser_newanalysis.add_argument("name")
    parser_newanalysis.add_argument("--projectdir")
    args = parser.parse_args()
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    if args.command == "newproject":
        newproject(args.projectdir, zettel=args.zettel)
    elif args.command == "newanalysis":
        newanalysis(args.name, projectdir=args.projectdir)


if __name__ == "__main__":
    main()
