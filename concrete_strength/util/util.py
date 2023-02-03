from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
import yaml
import numpy as np
import pandas as pd
import dill

def load_object(file_path:str):
    """
    file_path:str file path 
    """
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise ConcreteException(e,sys) from e

def save_object(file_path:str,obj:object):
    """
    file_path: destination to save the object
    obj : any object
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise ConcreteException(e,sys) from e

def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numoy array data to file
    file_path : location of file to save data
    array: np.array having data init
    """
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise ConcreteException(e,sys) from e

def load_numpy_array_data(file_path:str)->np.array:
    """
    file_path: str location of file to load
    return : np.array data
    """

    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise ConcreteException(e,sys) from e

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


def write_yaml_file(file_path:str,data:dict=None):
    """
    write content into yaml file
    file_path: destination file
    data: dictionary content
    """
    try:
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise ConcreteException(e,sys) from e

