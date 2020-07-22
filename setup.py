#!/usr/bin/env python3

from distutils.core import setup

# requirements
with open("requirements.txt") as requirements:
    req = [i.strip() for i in requirements]

setup(
    name="pyetrade",
    version="1.2.0",
    description="eTrade API wrappers",
    author="Jesse Cooper",
    author_email="jesse_cooper@codeholics.com",
    url="https://github.com/jessecooper/pyetrade",
    license="GPLv3",
    packages=["pyetrade"],
    package_dir={"pyetrade": "pyetrade"},
    install_requires=req,
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
        "Topic :: Software Development :: Libraries",
    ],
)
