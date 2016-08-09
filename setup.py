#!/usr/bin/env python

import os
from distutils.util import convert_path
from setuptools import setup, find_packages

location = os.path.abspath(os.path.dirname(__file__))
with open('README.md') as readme:
    description = readme.read()
metadata = dict()
with open(convert_path('src/telemetryserver/version.py')) as metadata_file:
    exec(metadata_file.read(), metadata)


setup(
    name='telemetryserver',
    version=metadata['__version__'],

    description='Simple telemetry server',
    long_description=description,

    url='https://github.com/arcan1s/telemetry-server',
    author='Evgeniy Alekseev',
    author_email='esalexeev@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance'
    ],

    keywords='server telemetry',

    packages=find_packages('src', exclude=['bin']),
    package_dir={'': 'src'},
    data_files=[
        ('share/telemetryserver', ['src/etc/telemetry-server.cfg'])
    ],
    scripts=[
        'src/bin/telemetry-server'
    ],

    zip_safe=False
)
