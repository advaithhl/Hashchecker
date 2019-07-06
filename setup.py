import setuptools
from hclib.help_strings import cli_help

with open('README.md', 'r') as fh:
    long_description = fh.read().strip()

INSTALL_REQUIRES = (
    'click>=7.0',
    'colorama>=0.4.1',
    'tabulate>=0.8.3',
)

VERSION = '1.0.1'


setuptools.setup(
    name="hashchecker",
    version=VERSION,
    author="Advaith H L",
    author_email="niceadvaith@gmail.com",
    description=cli_help.strip(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/advaithhl/Hashchecker",
    license='GPLv3',
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points='''
        [console_scripts]
        hashchecker=hclib.hashchecker:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
