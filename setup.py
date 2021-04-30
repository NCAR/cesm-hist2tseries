#!/usr/bin/env python3

"""The setup script."""

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

with open('README.md') as f:
    long_description = f.read()
setup(
    maintainer='ESDS Team',
    maintainer_email='esds@ucar.edu',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ],
    description='Tools for converting Community Earth System Model (CESM) output from history to timeseries files.',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description_content_type='text/markdown',
    long_description=long_description,
    include_package_data=True,
    keywords='CESM',
    name='cesm-hist2tseries',
    packages=find_packages(include=['cesm_hist2tseries', 'cesm_hist2tseries.*']),
    entry_points={
        'console_scripts': [
            'cesm-hist2tseries = cesm_hist2tseries.cli:main',
        ]
    },
    url='https://github.com/NCAR/cesm-hist2tseries',
    project_urls={
        'Documentation': 'https://github.com/NCAR/cesm-hist2tseries',
        'Source': 'https://github.com/NCAR/cesm-hist2tseries',
        'Tracker': 'https://github.com/NCAR/cesm-hist2tseries/issues',
    },
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'dirty-tag',
    },
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0'],
    zip_safe=False,
)
