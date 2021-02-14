from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Display',
    ext_modules=cythonize("Display.pyx"),
    zip_safe=False,
)