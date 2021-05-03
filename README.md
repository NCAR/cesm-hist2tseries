# cesm-hist2tseries

- [cesm-hist2tseries](#cesm-hist2tseries)
  - [Badges](#badges)
  - [Motivation](#motivation)
  - [What are "history files"? What are "timeseries files"?](#what-are-history-files-what-are-timeseries-files)
  - [Installation (TODO)](#installation-todo)

## Badges

| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![GitHub Workflow Status][github-lint-badge]][github-lint-link] [![Code Coverage Status][codecov-badge]][codecov-link] |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                                                    [![Documentation Status][rtd-badge]][rtd-link]                                                                    |
| **Package** |                                                         [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                         |
| **License** |                                                                        [![License][license-badge]][repo-link]                                                                        |

## Motivation

This tool is meant to be used for one specific task - converting [Community Earth System Model (CESM) output](https://www.cesm.ucar.edu/) from history to timeseries files.

This a common part of the post-processing workflow, and something that typically involves running a set of bash scripts, can be tough to reproduce and require a fair amount of modification.

This tool aims to fill a need for an open-source, well-documented tool for helping with this model post-processing step.

## What are "history files"? What are "timeseries files"?

CESM output is typically formatted in history files which include **_all model output fields_** organized into a single file for each timestep. This format can be difficult to deal with reading in

## Installation (TODO)

[github-ci-badge]: https://img.shields.io/github/workflow/status/NCAR/cesm-hist2tseries/CI?label=CI&logo=github&style=for-the-badge
[github-lint-badge]: https://img.shields.io/github/workflow/status/NCAR/cesm-hist2tseries/linting?label=linting&logo=github&style=for-the-badge
[github-ci-link]: https://github.com/NCAR/cesm-hist2tseries/actions?query=workflow%3ACI
[github-lint-link]: https://github.com/NCAR/cesm-hist2tseries/actions?query=workflow%3Alinting
[codecov-badge]: https://img.shields.io/codecov/c/github/NCAR/cesm-hist2tseries.svg?logo=codecov&style=for-the-badge
[codecov-link]: https://codecov.io/gh/NCAR/cesm-hist2tseries
[rtd-badge]: https://img.shields.io/readthedocs/cesm-hist2tseries/latest.svg?style=for-the-badge
[rtd-link]: https://cesm-hist2tseries.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/cesm-hist2tseries?logo=pypi&style=for-the-badge
[pypi-link]: https://pypi.org/project/cesm-hist2tseries
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/cesm-hist2tseries?logo=anaconda&style=for-the-badge
[conda-link]: https://anaconda.org/conda-forge/cesm-hist2tseries
[license-badge]: https://img.shields.io/github/license/NCAR/cesm-hist2tseries?style=for-the-badge
[repo-link]: https://github.com/NCAR/cesm-hist2tseries
