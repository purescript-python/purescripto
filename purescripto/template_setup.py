def gen_setup():
    meta_setup = r"""
import sys
import os
from setuptools import setup
from pathlib import Path
from purescripto.version import __version__
readme = ''

setup(
    name='pspy-executable',
    version=__version__,
    keywords="",  # keywords of your project that separated by comma ","
    description="",  # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.5.0',
    url='https://github.com/purescript-python/installer',
    author='thautawarm',
    author_email='twshere@outlook.com',
    packages=['pspy_executable'],
    install_requires=[],
    package_data={
        'pspy_executable': [
            each.name for each in Path('pspy_executable').iterdir()
            if each.name.startswith('pspy')
        ]
    },
    entry_points={"console_scripts": [
        "pspy-blueprint=pspy_executable:exe",
        "pspy-blueprint-check=pspy_executable:check"
    ]},
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)
"""
    print(meta_setup)

def gen_init():
    meta_init = r"""
def exe():
    from pathlib import Path
    from subprocess import call
    import os
    import sys
    exe_file = os.name == "nt" and "pspy-blueprint.exe" or "pspy-blueprint"
    cmd = str((Path(__file__).parent / exe_file).absolute())
    call([cmd, *sys.argv[1:]])

def check():
    print("pspy-executable installed")
"""
    print(meta_init)