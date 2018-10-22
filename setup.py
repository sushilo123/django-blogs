from setuptools import setup
from blogs import __version__

def readfile(filename):
    return open(filename, 'r').read()

print(__version__)
long_description = readfile('README.md')

setup(
    version=__version__,
    name='django-blogs',
    description='Django blogging with medium style editor',
    long_description=long_description,
    url='https://github.com/arjunsinghy96/django-blogs',
    author='Arjun Singh Yadav',
    author_email='arjunsinghy96@gmail.com',
    license='MIT',
    keywords='django blogs medium blog',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
    packages=['blogs']
    )
