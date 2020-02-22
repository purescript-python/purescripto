from setuptools import setup
from pathlib import Path
import sys
import os

version = 0.4
with Path('README.md').open() as readme:
    readme = readme.read()

# class BinaryDistribution(Distribution):
#     """https://stackoverflow.com/questions/35112511/pip-setup-py-bdist-wheel-no-longer-builds-forced-non-pure-wheels"""
#     def has_ext_modules(_):
#         return True
#
#     def is_pure(_):
#         return False
#


def select_os(plat: str):
    plat = plat.lower()
    assert plat in ('win64', 'linux64',
                    'macos'), OSError("Not supported platform {}".format(plat))
    return plat


platform_tags = {
    'linux64': 'linux_x86_64',
    'win64': 'win-amd64',
    'macos': 'macosx'
}

PLAT = os.environ['PLAT']
CPY = os.environ['CPY']
platform_tag = platform_tags[PLAT]

sys.argv.extend(['--python-tag', 'cp' + CPY, '--plat-name', platform_tag])
plat_dir = select_os(PLAT)

executables = [
    os.path.join(plat_dir, each.name)
    for each in (Path('pspyblueprint') / plat_dir).iterdir()
    if each.name.startswith('pspy')
]
if not executables:
    raise ValueError("No binary releases in bin/{}".format(plat_dir))

setup(
    # distclass=BinaryDistribution,
    name='purescripto',
    version=version if isinstance(version, str) else str(version),
    keywords="",  # keywords of your project that separated by comma ","
    description="",  # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.5',
    url='https://github.com/purescript-python/purescripto',
    author='thautawarm',
    author_email='twshere@outlook.com',
    packages=[
        'purescripto',
        'pspyblueprint',
        'pspyblueprint.{}'.format(plat_dir),
    ],
    entry_points={
        "console_scripts": [
            'pspy=purescripto.pspy:main',
            'pspy-blueprint=pspyblueprint.{}.blueprint:main'.format(plat_dir),
        ]
    },
    # above option specifies what commands to install,
    # e.g: entry_points={"console_scripts": ["yapypy=yapypy.cmd:compiler"]}
    install_requires=[
        'painless-import-extension',
        'pysexpr',
        'wisepy2',
        'gitpython',
    ],  # dependencies
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    package_data={'pspyblueprint': executables},
    zip_safe=False,
)
