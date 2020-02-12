#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
        name='qotto-common',
        version='0',
        url='https://github.com/qotto/common',
        license='Proprietary',
        author='Qotto',
        author_email='contact@qotto.net',
        description='Qotto/common',
        packages=['common'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Django >= 1.10',
        ],
        classifiers=[
            'Intended Audience :: Developers',
            'License :: Other/Proprietary License',
            'Programming Language :: Python :: 3.6',
        ],
    )
