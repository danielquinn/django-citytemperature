#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

from distutils.core import setup


rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_version():
    initfile = open(rel_file("src", "citytemp", "__init__.py")).read()
    return re.search(r"__version__ = \"([^\"]+)\"", initfile).group(1)


setup(
    name="django-citytemperature",
    version=get_version(),
    author="Daniel Quinn",
    author_email="code@danielquinn.org",
    url="http://github.com/danielquinn/django-citytemperature",
    description="A collection of mean temperatures for cities all over the world. There's some high/low data in there too, but not for every city.",
    packages=("citytemp",),
    package_dir={"": "src"},
    requires=("django (>=1.3)",),
    classifiers=[
	"Development Status :: 3 - Alpha",
	"Framework :: Django",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU Affero General Public License v3",
	"Natural Language :: English",
	"Programming Language :: Python :: 2.6",
	"Programming Language :: Python :: 2.7"
	"Programming Language :: Python :: 3"
    ],
)
