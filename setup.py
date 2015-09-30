from setuptools import find_packages, setup

setup(
    name='Henson-SQS',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto3>=1.1.1',
        'Henson>=0.3.0',
        'lazy>=1.2',
    ],
    tests_require=[
        'tox',
    ],
)
