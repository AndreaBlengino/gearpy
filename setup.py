from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name = 'gearpy',
      version = '0.0.1',
      description = "A python package for mechanical transmission analysis",
      packages = find_packages(where = '.'),
      py_modules = ['__init__'],
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author = 'Andrea Blengino',
      author_email = 'ing.andrea.blengino@gmail.com',
      extras_require = {'dev': ['sphinx >= 7.2.6',
                                'tox >= 4.11.3',
                                'twine >= 4.0.2']},
      python_requires = '>=3.9')
