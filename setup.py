from setuptools import find_packages, setup
import subprocess

version = subprocess.run(['git', 'describe', '--tags'], stdout = subprocess.PIPE).stdout.decode('utf-8').strip()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name = 'gearpy',
      version = version,
      description = "A python package for mechanical transmission analysis",
      packages = find_packages(where = '.'),
      py_modules = ['__init__', 'utils'],
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      url = 'https://github.com/AndreaBlengino/gearpy',
      project_urls = {'Source': 'https://github.com/AndreaBlengino/gearpy',
                      'Tracker': 'https://github.com/AndreaBlengino/gearpy/issues'},
      author = 'Andrea Blengino',
      author_email = 'ing.andrea.blengino@gmail.com',
      license = 'GNU GPL3',
      classifiers = ['Intended Audience :: Education',
                     'Intended Audience :: Manufacturing',
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.9',
                     'Programming Language :: Python :: 3.10',
                     'Programming Language :: Python :: 3.11',
                     'Topic :: Scientific/Engineering'],
      install_requires = ['numpy >= 1.26.0'],
      extras_require = {'dev': ['sphinx >= 7.2.6',
                                'tox >= 4.11.3',
                                'hypothesis >= 6.87.1',
                                'twine >= 4.0.2']},
      python_requires = '>=3.9, <3.12')
