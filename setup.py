# -*- coding: utf-8 -*-
# Copyright (c) 2021 The Project GNOME Pomodoro Tracking Authors
import sys
import os
from shutil import rmtree
from setuptools import setup, Command, find_packages

class PublishCommand(Command):

    user_options = [
        ('testpypi', 't', "Publish on https://test.pypi.org/")
    ]

    def initialize_options(self):
        self.testpypi = 0

    def finalize_options(self):
        pass

    def run(self):

        try:
            print("Removing previous builds ...")
            rmtree("./dist")
        except OSError:
            pass

        print("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal"
                  .format(sys.executable))

        print("Uploading the package to PyPi via Twine…")

        if self.testpypi:
            os.system("twine upload --repository testpypi dist/*")
        else:
            os.system("twine upload dist/*")

long_description = ""
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    for line in f.readlines():
        requirements.append(line.replace('\n', ''))

setup(
    name="gnome-pomodoro-tracking",
    version="4.0.3",
    url="https://github.com/gnome-pomodoro/gnome-pomodoro-tracking",
    author="Jose Hbez",
    author_email="dev@josehbez.com",
    description="Connect your Pomodoros to popular time tracking services.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": ["gnome-pomodoro-tracking=gnome_pomodoro_tracking.__main__:main"]
    },
    install_requires=requirements,
    license="MIT",
    classifiers=[

        "Environment :: Console",

        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Operating System :: POSIX :: Linux",

        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Utilities",
    ],
    cmdclass={
       "publish": PublishCommand
    }
)
