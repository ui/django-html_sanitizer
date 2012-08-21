# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-html_sanitizer',
    version='0.1.3',
    author='Selwin Ong',
    author_email='selwin.ong@gmail.com',
    packages=['sanitizer'],
    package_data = { '': ['README.rst'],
                    'sanitizer': ['templatetags/*.py']},
    url='https://github.com/ui/django-html_sanitizer',
    license='MIT',
    description='Provides a set of HTML cleaning utilities for django models, forms and templates.',
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['django', 'bleach'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
    ]
)