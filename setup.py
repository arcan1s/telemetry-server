#!/usr/bin/env python

import os
from setuptools import setup, find_packages

location = os.path.abspath(os.path.dirname(__file__))
with open('README.md') as readme:
    description = readme.read()


setup(
    name='telemetryserver',
    version='0.9.0',

    description='Simple telemetry server',
    long_description=description,

    url='https://github.com/arcan1s/simple-telemetry-server',
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
