from setuptools import setup, find_packages

setup(
    name='gmail2pubsub',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-cloud-pubsub',
        'google-auth',
        'google-api-python-client',
        'pytz',
        'dateparser'
    ],
    entry_points={
        'console_scripts': [
            'gmail2pubsub=main:main',
        ],
    },
)
