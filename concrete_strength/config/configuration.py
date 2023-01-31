from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *
from concrete_strength.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig

class Configuration:
    def __init__(self,config_file_path=CONFIG_FILE_PATH,
                current_time_stamp:str=CURRENT_TIME_STAMP)->None:
        try:
            self.config_info=read_yaml_file(config_file_path)
            self.trainig_pipeline_config=self.get_training_pipeline_config()
            self.time_stamp=current_time_stamp
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,
                                        training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR])

            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            
            logging.info(f"Training pipeline config: {training_pipeline_config}")

            return training_pipeline_config
        except Exception as e:
            raise ConcreteException(e,sys) from e
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            pass
        except Exception as e:
            raise ConcreteException(e,sys) from e
    def get_data_validation_config(self):
        pass
    def get_data_transformation_config(self):
        pass
    def get_model_trainer_config(self):
        pass
    def get_model_evaluation_config(self):
        pass
    def get_model_pusher_config(self):
        pass