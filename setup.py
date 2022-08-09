#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="fgen",
        version="0.0.1",
        author="stfujnkk",
        description="Extensible template parser",
        license="MIT",
        packages=find_packages(),
        install_requires=[
            'Jinja2>=3.0.0',
            'setuptools>=16.0.0'
        ],
        entry_points={
            'console_scripts': [
                'fgen = fgen.__main__:main'
            ]
        }
    )