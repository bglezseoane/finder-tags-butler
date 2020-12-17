# -*- coding: utf-8 -*-

###########################################################
# Finder Tags Butler
#
# Synchronize Mac OS Finder tags between several machines
#
# Copyright 2020 Borja González Seoane
#
# Contact: garaje@glezseoane.es
###########################################################

from setuptools import setup


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

version = "0.1.dev2"

setup(
    name="finder-tags-butler",
    version=version,
    packages=["finder_tags_butler"],
    entry_points={"console_scripts": ["ftbutler=finder_tags_butler.__main__:main",],},
    python_requires=">=3.8.5",
    install_requires=["pyyaml==5.3.1", "mac-tag==0.0.0"],
    data_files=[("", ["requirements.txt"]), ("", ["README.md"]), ("", ["LICENSE"]),],
    url="https://github.com/bglezseoane/finder-tags-butler",
    download_url=f"https://github.com/bglezseoane/finder-tags-butler/archive/{version}.tar.gz",
    license="LICENSE",
    author="Borja González Seoane",
    author_email="garaje@glezseoane.es",
    description="Synchronize Mac OS Finder tags between several machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Topic :: Utilities",
        "Topic :: System :: Filesystems",
    ],
)
