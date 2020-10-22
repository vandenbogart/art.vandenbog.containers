from setuptools import setup, find_packages

requires = [
    "requests",
    "cython",
    "faust[rocksdb,debug]",
    "yarl<1.6.0,>=1.0",
    "multidict<5.0,>=4.5",
    "gitpython",
    "beautifulsoup4",
]

setup(
    name='faust_app',
    version='1.0',
    description='faust app  with docker container',
    author='Eric Bogard',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'faust_app = faustapp.app:main',
        ],
    },
)
