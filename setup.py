# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:15:15 2021

@author: TimmyR
"""
from setuptools import setup

setup(
    name = 'minesweeper',
    version = '0.0.1',
    author = 'TimmyR',
    packages = ['minesweeper'],
    entry_points = {
        'console_scripts': [
            'minesweeper = minesweeper.__main__:main'
        ]
    })