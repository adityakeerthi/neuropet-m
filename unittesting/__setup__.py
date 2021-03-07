from setuptools import setup
from Cython.Build import cythonize

setup(
    name='neuropetm',
    ext_modules=cythonize("neuropetm.pyx"),
    zip_safe=False,
)