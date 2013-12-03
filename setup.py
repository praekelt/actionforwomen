from setuptools import setup, find_packages

setup(
    name='mama',
    version='0.3.5',
    description='Mama Django project.',
    long_description=open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/mama',
    packages=find_packages(),
    dependency_links=[
    ],
    install_requires=[
        'django==1.4.5',
        'django-category==0.1',
        'django-debug-toolbar',
        'django-export',
        'django-generate',
        'django-google-analytics-app',
        'django-google-credentials',
        'django-haystack==1.2.7',
        # install via requirements.pip, django-moderator is broken.
        # install 0.0.4.1 from GitHub tag which has a fix for the Admin.
        # 'django-moderator>=0.0.4',
        'django-preferences',
        'django-sites-groups',
        'django-snippetscream',
        'django-south-admin',
        'django-registration==0.8',
        'django-userprofile>=0.0.6',
        'django-registration==0.8',
        'django-ckeditor',
        'gunicorn',
        'jmbo==0.5.5',
        'jmbo-poll>=0.0.9',
        'jmbo-post',
        'kombu==2.4.7',
        'celery==3.0.11',
        'photon',
        'psycopg2',
        'python-ambient',
        'python-dateutil',
        'python-memcached',
        'raven',
        'south',
        'Whoosh==2.4.1',
        #'python-mxit',
        'django-mxit',
    ],
    tests_require=[
        'django-setuptest',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers=[
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
