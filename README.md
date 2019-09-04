# conda-diff

[![Build Status](https://travis-ci.org/k-dominik/conda-diff.svg?branch=master)](https://travis-ci.org/k-dominik/conda-diff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Current bin version](https://anaconda.org/kdominik/conda-diff/badges/version.svg)](https://anaconda.org/kdominik/conda-diff)

Command line tool to compare conda environments

## Installation

```bash
$ conda install -c kdominik -c conda-forge conda-diff
```

## Usage

Usage is still very limited. You can two compare different existing conda environments and/or conda lists generated with `conda list --json` or `conda create --json` (e.g. from dry-run).

```bash
$ conda create -n tmp --dry-run --json -c conda-forge python=3.6 > py36.json
$ conda create -n tmp --dry-run --json -c conda-forge python=3.7 > py37.json
$ conda-diff py36.json py37.json

Diff report for environments py36.json and py37.json:

Common Packages (without diff)
------------------------------
  _libgcc_mutex
  ca-certificates
  libffi
  libgcc-ng
  libstdcxx-ng
  ncurses
  openssl
  readline
  sqlite
  tk
  xz
  zlib

Common Packages (with diff)
---------------------------
  certifi
  pip
  python
  setuptools
  wheel

Packages Only In py36.json:
--------------------------


Packages Only In py37.json:
--------------------------
  bzip2

```
Increase verbosity to get more detailed output:
```bash
$ conda-diff py36.json py37.json -vv

Diff report for environments py36.json and py37.json:

 ... (abbreviated for docs)

Common Packages (with diff)
---------------------------
  certifi
    build_string: py36_1 -> py37_1
    dist_name: certifi-2019.6.16-py36_1 -> certifi-2019.6.16-py37_1
  pip
    build_string: py36_0 -> py37_0
    dist_name: pip-19.2.3-py36_0 -> pip-19.2.3-py37_0
  python
    build_number: 1005 -> 1
    build_string: h357f687_1005 -> h33d41f4_1
    dist_name: python-3.6.7-h357f687_1005 -> python-3.7.3-h33d41f4_1
    version: 3.6.7 -> 3.7.3
  setuptools
    build_string: py36_0 -> py37_0
    dist_name: setuptools-41.2.0-py36_0 -> setuptools-41.2.0-py37_0
  wheel
    build_string: py36_0 -> py37_0
    dist_name: wheel-0.33.6-py36_0 -> wheel-0.33.6-py37_0

Packages Only In py36.json:
--------------------------


Packages Only In py37.json:
--------------------------
  bzip2

```

Todos:

- [ ] add more, better formatters
  - [ ] `.md` output
- [ ] add json output
