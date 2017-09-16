#! /usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

config = {
    'description': 'Monitor system with python',
    'author': 'Deba and Mohit',
    'url': 'https://gitlab.corp.apple.com/debabrat_panda/py-monit.git',
    'download_url': 'https://gitlab.corp.apple.com/debabrat_panda/py-monit.git',
    'author_email': 'debabrat_panda@apple.com, mohit_mohit@apple.com',
    'version': '0.1',
    'install_requires': ['nose','zmq','psutil','bottle'],
    'packages': ['src/resources','src','src/messaging','src/server','src/system','src/utils'],
    'scripts': [],
    'name': 'py-monit',
    'include_package_data': True,
    'zip_safe': False,
    'long_description': readme()
}

setup(**config)