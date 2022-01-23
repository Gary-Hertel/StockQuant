# -*- coding:utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name="stockquant",
    version="1.1.0",
    packages=[
        "stockquant",
        "stockquant/source",
        "stockquant/utils"
    ],
    platforms="any",
    description="Professional quant framework",
    url="https://github.com/Gary-Hertel/StockQuant",
    author="Gary-Hertel",
    author_email="garyhertel@foxmail.com",
    license="MIT",
    keywords=[
        "stockquant", "quant", "framework"
    ],
    install_requires=[
        "numpy",
        "requests",
        "concurrent-log-handler",
        "colorlog",
        "pandas",
        "matplotlib",
        "tushare",
        "baostock",
        "finplot",
        "easytrader",
        "PyQt5==5.14.1"
    ]
)