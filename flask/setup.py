from setuptools import setup, find_packages

requires = [
    "requests",
    "flask",
    "kafka-python",
    "beautifulsoup4",
    "pymongo",
    "gitpython",
    "pylint",
]

setup(
    name='flask_app',
    version='1.0',
    description='flask app with docker container',
    author='Eric Bogard',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
)