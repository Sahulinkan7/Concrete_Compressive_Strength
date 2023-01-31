from setuptools import setup,find_packages
from typing import List

PROJECT_NAME="Concrete_Compressive_Strength_Prediction"
VERSION="0.0.1"
AUTHOR="Linkan Kumar Sahu"
DESCRIPTION="A machine learning project to predict the strength of a concrete mixture"

REQUIREMENT_FILE_NAME="requirements.txt"

HYPHEN_E_DOT="-e ."

def get_requirement_list()->List[str]:
    """
    This function will return the list of libraries mentioned in requirements.txt file.
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list=requirement_file.readlines()
        requirement_list=[requirement_name.replace("\n","") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirement_list()
)