from setuptools import setup, find_packages

setup(
    name='mama',
    version='0.0.1',
    description='Mama Django project.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/mama',
    packages = find_packages(),
    dependency_links = [
        'https://github.com/praekelt/django-sites-groups/tarball/0.1.2#egg=django-sites-groups-0.1.2'
    ],
    install_requires=[
        'django-sites-groups==0.1.2',
        'django>=1.4',
        'django-generate',
        'django-preferences',
        'django-userprofile',
        'django-snippetscream',
        'flup',
        'jmbo',
        'jmbo-poll',
        'jmbo-post',
        'psycopg2',
        'south',
    ],
    tests_require=[
        'django-setuptest',
    ],
    test_suite="setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
