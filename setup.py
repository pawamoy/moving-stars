#!/usr/bin/env python

from __future__ import absolute_import, print_function

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


setup(
    name='moving-stars',
    version='0.1.0',
    license='ISC',
    description='Copy the stars you gave on different Git services.',
    author='Timothée Mazzucotelli',
    author_email='pawamoy@pm.me',
    url='https://gitlab.com/pawamoy/moving-stars',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords=[
        'github', 'gitlab', '#movingtogitlab', 'stars', 'git',
    ],
    install_requires=[
        'requests', 'colorama', 'pytoml'
    ],
    entry_points={
        'console_scripts': [
            'move-stars = moving_stars.cli:main',
        ],
    },
)
