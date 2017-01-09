import os
import setuptools

setuptools.setup(
    name='ssproc',
    version='0.0.1',
    packages=setuptools.find_packages(),
    author='Johanna Hansen',
    author_email='jhansen@cim.mcgill.ca',
    description='Data processing functions for working with sonar data',
    long_description=open(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'README.md')).read(),
    license='BSD 3-clause',
    url='http://github.com/ssproc/ssproc/',
    package_data={
    },
    install_requires=['numpy',
                      'scipy',
                      ],
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Topic :: Scientific/Engineering'],
)
