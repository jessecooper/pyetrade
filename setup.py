#!/usr/bin/env python3

from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = "1.3.6"
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# requirements
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]

setup(
    name="pyetrade",
    version=__version__,
    description="eTrade API wrappers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jesse Cooper",
    author_email="jesse_cooper@codeholics.com",
    url="https://github.com/jessecooper/pyetrade",
    license="GPLv3",
    packages=find_packages(exclude=["docs", "test*"]),
    install_requires=install_requires,
    platforms=["any"],
    keywords=["etrade", "pyetrade", "stocks"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
