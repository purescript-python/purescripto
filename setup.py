from setuptools import setup, find_packages
from datetime import datetime
from pathlib import Path

version = 0.2
with Path('README.md').open() as readme:
    readme = readme.read()

setup(
    name='purescripto',
    version=version if isinstance(version, str) else str(version),
    keywords="",  # keywords of your project that separated by comma ","
    description="",  # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.5',
    url='https://github.com/thautawarm/purescripto',
    author='thautawarm',
    author_email='twshere@outlook.com',
    packages=find_packages(),
    entry_points={"console_scripts": ['pspy=purescripto.pspy:main']},
    # above option specifies what commands to install,
    # e.g: entry_points={"console_scripts": ["yapypy=yapypy.cmd:compiler"]}
    install_requires=[
        'painless-import-extension',
        'pysexpr',
        'wisepy2',
        'gitpython',
        'diskcache'
    ],  # dependencies
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)
