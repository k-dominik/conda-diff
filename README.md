# conda-diff

[![Build Status](https://travis-ci.org/k-dominik/conda-diff.svg?branch=master)](https://travis-ci.org/k-dominik/conda-diff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

Todos:

- [ ] add more, better formatters
  - [ ] `.md` output
- [ ] add json output
