from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name = 'fuzzy_dempster_shafer',
    version = '0.01',
    description = 'Prediction algorithm based in Dempster-Shafer Fuzzy Logic and Bayesian principles',
    classifiers = ['Programming Language :: Python :: 3.5']
    url = 'https://github.com/phystistics/fuzzy_dempster_shafer',
    author = 'Austin Powell',
    author_email = 'powellaus10@gmail.com',
    license = 'MIT',
    zip_safe = False)
