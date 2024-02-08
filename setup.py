#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from wagtail_hallo import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail-hallo",
    version=__version__,
    description="Wagtail Hallo - The legacy richtext editor for Wagtail.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Wagtail core team",
    author_email="hello@wagtail.org",
    url="https://github.com/wagtail-nest/wagtail-hallo",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 5",
        "Framework :: Wagtail :: 6",
    ],
    install_requires=[
        "Django>=3.2,<6.0",
        "Wagtail>=4.0,<7.0",
    ],
    extras_require={
        "testing": ["dj-database-url==0.5.0", "freezegun==0.3.15"],
    },
    zip_safe=False,
)
