from setuptools import setup, find_packages

setup(
    name='python_kt_2',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='контрольная точка №2',
    long_description=open('README.md').read(),
    install_requires=['flask', 'typer'],
    url='https://github.com/ITHUB-SPB/ithub-python-project-2/',
    author='saint hubs community',
    author_email='daslef93@gmail.com',
    entry_points={
        'console_scripts': [
            'cli = python_kt_2.cli:app',
            'web = python_kt_2.web:main'
        ],
    },
)