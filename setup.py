# pylint: disable=missing-module-docstring

# This is just to make zappa work.
# See also: https://stackoverflow.com/a/49183765

from setuptools import setup

setup(
    name='kha',
    packages=['kha'],
    include_package_data=True,
    install_requires=['Flask'],
)
