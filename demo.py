from concrete_strength.config.configuration import Configuration
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *


def main():

    c=Configuration(config_file_path=r"config/config.yaml",current_time_stamp=CURRENT_TIME_STAMP)
    print(c.get_training_pipeline_config())


main()