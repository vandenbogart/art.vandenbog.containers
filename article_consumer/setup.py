from setuptools import setup, find_packages

requires = [
    "kafka-python",
    "pymongo",
]

setup(
    name='Article Consumer',
    version='1.0',
    description='Consumes from the articles topic',
    author='Eric Bogard',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
)
