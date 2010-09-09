"""
Setup file for django-critic
"""
import os
from setuptools import setup, find_packages
import critic

try:
    REQS = open(
        os.path.join(os.path.dirname(__file__),'requirements.txt')).read()
except (IOError, OSError):
    REQS = ''

setup(
    name = 'django-critic',
    version=critic.get_version(),
    description = 'A rating application.',
    author = 'Jose Soares',
    author_email = 'jsoares@washingtontimes.com',
    url = 'http://opensource.washingtontimes.com/projects/critic/',
    packages = find_packages(),
    include_package_data = True,
    install_requires = REQS,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
