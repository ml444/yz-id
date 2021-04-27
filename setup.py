#!/usr/bin/python3.6.8+
# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yzid",  # Replace with your own username
    version="0.1.0",
    author="cml",
    author_email="caimengli0660@gmail.com",
    description="An ID generator for distributed microservices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ml444/yz-id.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
