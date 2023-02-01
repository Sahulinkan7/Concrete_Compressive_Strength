from concrete_strength.config.configuration import Configuration
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *
from concrete_strength.component.data_ingestion import DataIngestion
from concrete_strength.component.data_validation import DataValidation


def main():

    c=Configuration(config_file_path=r"config/config.yaml",current_time_stamp=CURRENT_TIME_STAMP)
    print(c.get_training_pipeline_config())
    print(c.get_data_ingestion_config())
    d=DataIngestion(c.get_data_ingestion_config())
    v=DataValidation(d.initiate_data_ingestion(),c.get_data_validation_config())
    print(v.initiate_data_validation())



main()