import re
from setuptools import setup, find_packages

file_content = None
with open('authme/__init__.py') as f:
    file_content = f.read()

search_for = lambda match: re.search(rf'^{match}\s*=\s*[\'"]([^\'"]*)[\'"]', file_content, re.MULTILINE).group(1)

name = search_for('__name__')
version = search_for('__version__')
author = search_for('__author__')
license = search_for('__license__')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name=name,
    version=version,
    author=author,
    url='https://github.com/legi0n/django-authme',
    license=license,
    description='Authentication utilities and systems for Django',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    keywords='django authentication login utilities',
    project_urls={
        'Source': 'https://github.com/legi0n/django-authme',
        'Issue tracker': 'https://github.com/legi0n/django-authme/issues',
    },
    python_requires='>=3.8',
    install_requires=[
        'django>=3.2'
    ],
    extras_require={
        'dev': [],
        'test': [],
    },
    packages=find_packages(),
)
