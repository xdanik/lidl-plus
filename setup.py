#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lidl-plus",
    version="0.1.12",
    author="Andre Basche",
    description="Fetch receipts and more from Lidl Plus",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Andre0512/lidl-plus",
    license="MIT",
    platforms="any",
    package_dir={"": "src"},
    packages=["lidlplus"],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["requests"],
    extras_require={
        "auth": [
            "selenium-wire",
            "webdriver-manager"
            "getuseragent",
            "oic"
        ]
    },
    entry_points={
        'console_scripts': [
            'lidl-plus = lidlplus.__main__:main',
        ]
    }
)
