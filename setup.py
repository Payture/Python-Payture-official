"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    #long_description = f.read()

setup(
    name='payture',
    version='0.0.17',

    description='Official Payture API',
    #long_description=long_description,

    url='https://github.com/Payture/Python-Payture-official',
    author='Soloveva Elena',
    author_email='elena.solovieva@payture.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',


        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='payments online-payments payture paytureapi transaction',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['payture'], #find_packages(exclude=['contrib', 'docs', 'tests']),
    package_dir={'payture': 'payturetypes'},
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests'],


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)