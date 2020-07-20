#!/usr/bin/env python
"""rb ldap automation"""

from importlib.machinery import SourceFileLoader
from io import open
from os import path

from setuptools import find_packages, setup


def load_requirements(requirements_file):
    """parse requirements.txt file"""
    requirements_path = path.join(
        path.abspath(path.dirname(__file__)), requirements_file
    )
    with open(requirements_path, encoding="utf-8") as f:
        return [
            line
            for line in f.readlines()
            if line and not line.startswith("--") and not line.startswith("#")
        ]


module = SourceFileLoader(
    fullname="version", path=path.join("src", "version.py")
).load_module()

requirements = load_requirements("requirements.txt")

setup(
    name=module.PACKAGE_NAME,
    description=module.PACKAGE_INFO,
    long_description=open("README.md").read(),
    author=module.__author__,
    author_email=module.TEAM_EMAIL,
    version=module.__version__,
    url=module.PROJECT_HOME,
    license=module.PACKAGE_LICENSE,
    python_requires=">3.8.*, <4",
    packages=find_packages(exclude=["test"]),
    install_requires=requirements,
    entry_points={"console_scripts": ["rbldap=src.__main__:main"]},
    setup_requires=[],
    tests_require=requirements,
)
