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
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Framework :: Django',
        'Typing :: Typed',
        'Topic :: Internet :: WWW/HTTP',
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
        'test': [
            'factory_boy>=3.2.1',
            'Faker>=13.14.0',
        ],
    },
    packages=find_packages(exclude=['tests']),
)
