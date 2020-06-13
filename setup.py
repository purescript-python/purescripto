from setuptools import setup
from pathlib import Path
from purescripto.version import __version__ as version

with Path("README.md").open() as readme:
    readme = readme.read()

setup(
    # distclass=BinaryDistribution,
    name="purescripto",
    version=version if isinstance(version, str) else str(version),
    keywords="",  # keywords of your project that separated by comma ","
    description="",  # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license="mit",
    python_requires=">=3.5",
    url="https://github.com/purescript-python/purescripto",
    author="thautawarm",
    author_email="twshere@outlook.com",
    packages=["purescripto"],
    entry_points={
        "console_scripts": [
            "pspy=purescripto.pspy:cmd_pspy",
            "pspy-get-binary=purescripto.pspy:cmd_get_binary",
            "pspy-gen-setup=purescripto.pspy:cmd_gen_setup",
            "pspy-gen-init=purescripto.pspy:cmd_gen_init",
        ]
    },
    # above option specifies what commands to install,
    # e.g: entry_points={"console_scripts": ["yapypy=yapypy.cmd:compiler"]}
    install_requires=[
        "painless-import-extension",
        "pysexpr>=0.5,<=0.6",
        "wisepy2>=1.1.1",
        "gitpython",
        "requests"
    ],  # dependencies
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)
