from setuptools import setup, find_packages

setup(
    name='mama',
    version='0.1.4',
    description='Mama Django project.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/mama',
    packages = find_packages(),
    dependency_links = [
    ],
    install_requires=[
        'django>=1.4',
        'django-generate',
        'django-google-credentials',
        'django-haystack',
        'django-moderator>=0.0.4',
        'django-preferences',
        'django-sites-groups',
        'django-snippetscream',
        'django-south-admin',
        'django-userprofile>=0.0.6',
        'flup',
        'jmbo>=0.5.3',
        'jmbo-poll>=0.0.5',
        'jmbo-post',
        'photon',
        'psycopg2',
        'python-ambient',
        'south',
        'whoosh',
    ],
    tests_require=[
        'django-setuptest',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
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
