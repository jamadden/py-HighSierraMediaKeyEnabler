import codecs
from setuptools import setup, find_packages

version = '0.0.1.dev0'

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
]

def _read(fname):
    with codecs.open(fname, encoding='UTF-8') as f:
        return f.read()

setup(
    name='py-HighSierraMediaKeyEnabler',
    version=version,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="Python version of HighSierraMediaKeyEnabler",
    long_description=_read('README.rst') + _read('CHANGES.rst'),
    license='Apache',
    keywords='macOS media key',
    url='https://github.com/jamadden/py-HighSierraMediaKeyEnabler',
    zip_safe=True,
    classifiers=[
        'Natural Language :: English',
        'Operating System :: macOS',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
	include_package_data=True,
    namespace_packages=['scs'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'pyobjc',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
    },
    entry_points=entry_points
)
