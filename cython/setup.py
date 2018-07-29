from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension("primality",
                sources=["cyprime.pyx", "gmp_prime.cpp"],
                libraries=["mpir"],
                library_dirs=[r"C:\mpir"],
                include_dirs=[r"C:\mpir"],
                language="c++")

setup(ext_modules=cythonize([ext]))
