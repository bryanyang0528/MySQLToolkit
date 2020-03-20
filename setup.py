#!/usr/bin/env python3

import os
import sys
from setuptools import setup

if sys.version_info < (3, 6):
    print("Python versions prior to 3.6 are not supported for pip installed MySQLToolkit.",
          file=sys.stderr)
    sys.exit(-1)

here = os.path.dirname(__file__)

try:
    exec(open(os.path.join(here, 'mysqltoolkit/version.py')).read())
except IOError:
    print("Failed to load mysqltoolkit version file for packaging.",
          file=sys.stderr)
    sys.exit(-1)

VERSION = __version__  # noqa

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setuptools_kwargs = {
    'install_requires': [
        'PyMySQL',
    ],
    'zip_safe': False,
}

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="mysqltoolkit",
    version=VERSION,
    description="A Python wrapper for simplify MySQL commends.",
    long_description=long_description,
    author="Bryan Yang",
    author_email="bryanyang0528@gmail.com",
    url="https://github.com/bryanyang0528/MySQLToolkit",
    license="MIT License",
    packages=[
        "mysqltoolkit"
    ],
    include_package_data=True,
    platforms=['any'],
    install_requires=['PyMySQL==0.9.3'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"]
)
