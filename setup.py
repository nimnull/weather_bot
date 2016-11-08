import codecs
import os
import re
import sys

from setuptools import setup


if sys.version_info < (3, 5, 1):
    raise RuntimeError("some_serial requires Python 3.5.1+")


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'some_serial', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


install_requires = [
    'aiohttp==1.1.1',
    'click>=6.6,<7',
    'pyserial>=3.2,<3.3',
    'pyserial-asyncio>=0.2',
    'pyaml>=16.11',
    'trafaret>=0.7,<0.8',
]

tests_require = install_requires + ['pytest']

args = dict(
    name='some_serial',
    version=version,
    description=('Chat bot for home weather station'),
    long_description='\n\n'.join((read('README.md'), )),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP'],
    author='Yehor Nazarkin',
    author_email='nimnull@gmail.com',
    url='https://github.com/nimnull/some_serial',
    license='Apache 2',
    packages=['some_serial'],
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run_serial = some_serial.main:run',
        ]
    }
)

setup(**args)
