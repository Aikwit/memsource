from setuptools import setup

setup(
name='memsource',
version='0.1.0',
author='Andraz Repar',
author_email='andraz@aikwit.com',
packages=['memsource'],
#scripts=['bin/script1','bin/script2'],
url='https://github.com/Aikwit/memsource',
license='LICENSE',
description='Aikwit memsource package',
long_description=open('README.md').read(),
install_requires=[
    "requests >= 2.28.0"
],
)