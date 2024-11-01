from setuptools import setup, find_packages

setup(
    name='cis6930fa24-project1',
    version='1.0',
    author='Thrisha Reddy Pagidi',
    author_email='pagidithrisha@ufl.edu',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

