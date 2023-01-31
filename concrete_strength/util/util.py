from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
import yaml

def read_yaml_file(file_path:str)->dict:
    """
    file_path : input file path to read yaml file content
    returns content as dictionary
    """
    try:
        with open(file_path,"rb") as yaml_file:
            yaml_content=yaml.safe_load(yaml_file)
            return yaml_content
    except Exception as e:
        raise ConcreteException(e,sys) from e