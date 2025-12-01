from setuptools import setup, find_packages

setup(
    name='buddy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'groq',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'buddy=buddy.main:main',
        ],
    },
)
