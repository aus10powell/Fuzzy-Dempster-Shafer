from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name = 'fuzzy_dempster_shafer',
    version = '0.13',
    description = 'Prediction algorithm based in Dempster-Shafer Fuzzy Logic and Bayesian principles',
    long_description = 'This is an ongoing project to creating a machine learning classification package. \
    The highlight of this package will be the utilization of Dempster-Shafer theory to improve on classifications \
    from other methods such as logistic regression.',
    classifiers = ['Programming Language :: Python :: 3.5'],
    url = 'https://github.com/phystistics/fuzzy_dempster_shafer',
    test_suite = 'nose.collector',
    tests_require = ['nose'],
    author = 'Austin Powell',
    author_email = 'powellaus10@gmail.com',
    license = 'MIT',
    packages=['fuzzy_dempster_shafer'],
    install_requires = [
        'scipy',
        'pandas',
        'numpy',
        'sklearn'
    ],
    zip_safe = False)
