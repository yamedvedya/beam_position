#!/usr/bin/python3
import io
import os
from subprocess import check_output, STDOUT
from setuptools.command.install import install

from setuptools import setup, find_packages


# Package meta-data.
NAME = 'beam_position'
DESCRIPTION = 'Shows beam shift wrt reference position'
EMAIL = 'yury.matveev@desy.de'
AUTHOR = 'Yury Matveyev'
REQUIRES_PYTHON = '>=3.7'
VERSION = '0.0.1'

# What packages are required for this module to be executed?
REQUIRED = ['numpy']

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_dir={'beam_position': 'beam_position',
                 },
    package_data={
        'petra_viewer': ['beam_position/*.py'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='GPLv3',
    entry_points={
        'console_scripts': [
            'beam_position = beam_position:main',
        ],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 3 - Alpha'
    ],
)
