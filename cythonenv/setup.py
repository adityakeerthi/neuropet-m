from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Process',
    ext_modules=cythonize("Process.pyx"),
    zip_safe=False,
)