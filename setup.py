from setuptools import setup


setup(
    name='ensure-trailing-commas',
    description='pre-commit hook that ensures trailing commas for python',
    url='https://github.com/LiraNuna/py-ensure-trailing-commas',
    version='0.1.1',

    author='Liran Nuna',
    author_email='liranuna@gmail.com',

    packages=[
        'ensure_trailing_commas',
    ],
    install_requires=[
        'asttokens>=1.1.7',
    ],
    entry_points={
        'console_scripts': [
            'ensure-trailing-commas = ensure_trailing_commas.main:main',
        ],
    },
)
