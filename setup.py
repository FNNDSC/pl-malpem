from setuptools import setup
import re

_version_re = re.compile(r"(?<=^__version__ = (\"|'))(.+)(?=\"|')")

def get_version(rel_path: str) -> str:
    """
    Searches for the ``__version__ = `` line in a source code file.

    https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
    """
    with open(rel_path, 'r') as f:
        matches = map(_version_re.search, f)
        filtered = filter(lambda m: m is not None, matches)
        version = next(filtered, None)
        if version is None:
            raise RuntimeError(f'Could not find __version__ in {rel_path}')
        return version.group(0)


setup(
    name='malpem_cpl',
    version=get_version('malpem_cpl.py'),
    description='Brain MRI bias correction, extraction, and segmentation pipeline',
    author='Christian Ledig, BioMedIA, & FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-malpem',
    py_modules=['malpem_cpl'],
    install_requires=['chris_plugin==0.4.0'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'malpem_chris_wrapper = malpem_cpl:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    }
)
