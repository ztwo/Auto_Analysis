# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/16 下午3:25
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='Auto_Analysis',
    keywords='',
    version=1.0,
    packages=find_packages(),
    url='',
    license='MIT',
    author='joko',
    author_email='imjoko@gmail.com',
    description='',
    install_requires=[
        'pyyaml', 'matplotlib', 'Appium-Python-Client', 'selenium', 'termcolor'
    ]
)
