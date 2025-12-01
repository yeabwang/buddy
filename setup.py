from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='buddy-ai-cli',
    version='0.1.1',
    description='Your AI Coding Assistant CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yeab Wang',
    url='https://github.com/yeabwang/buddy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'groq',
        'python-dotenv',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'buddy=buddy.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
