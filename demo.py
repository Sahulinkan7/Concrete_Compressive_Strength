from concrete_strength.config.configuration import Configuration
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *
from concrete_strength.component.data_ingestion import DataIngestion


def main():

    c=Configuration(config_file_path=r"config/config.yaml",current_time_stamp=CURRENT_TIME_STAMP)
    print(c.get_training_pipeline_config())
    print(c.get_data_ingestion_config())
    d=DataIngestion(c.get_data_ingestion_config())
    print(d.initiate_data_ingestion())



main()