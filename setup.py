from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filepath:str)-> List[str]:
    requirements = []
    with open (filepath,'r') as fileobj:
        requirements = fileobj.readlines()
        # Strip newline characters and extra spaces
        requirements = [req.strip() for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='NLP_SA',
    version='0.1.0',
    description='An NLP project for product review sentiment analysis and classification',
    author='Rohit Dusane',
    author_email='stat.data247@example.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    python_requires='>=3.10',
)
