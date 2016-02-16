from setuptools import find_packages, setup

setup(
    name='Henson-SQS',
    version='0.2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto3>=1.1.1',
        'Henson>=0.5.0',
        'lazy>=1.2',
    ],
    tests_require=[
        'tox',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
