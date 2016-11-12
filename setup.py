#!/usr/bin/env python3

from setuptools import setup, find_packages
import io
import emails


with io.open('README.md', "rt", encoding='utf-8') as fp:
    long_description = fp.read()


setup(
    packages=find_packages(),
    include_package_data=True,
    name='django-fluo-emails',
    version=emails.__version__,
    description='emails on database',
    long_description=long_description,
    author=emails.__author__,
    author_email=emails.__email__,
    url='https://bitbucket.org/rsalmaso/django-fluo-emails',
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: JavaScript',
    ],
    install_requires=["django-fluo"],
    zip_safe=False,
)
