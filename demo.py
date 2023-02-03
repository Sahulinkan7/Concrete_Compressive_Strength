from concrete_strength.config.configuration import Configuration
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *
from concrete_strength.component.data_ingestion import DataIngestion
from concrete_strength.component.data_validation import DataValidation
from concrete_strength.component.data_transformation import DataTransformation
from concrete_strength.component.model_trainer import ModelTrainer


def main():

    c=Configuration(config_file_path=r"config/config.yaml",current_time_stamp=CURRENT_TIME_STAMP)
    d=DataIngestion(data_ingestion_config=c.get_data_ingestion_config())
    ingestion_artifact=d.initiate_data_ingestion()
    print(f"--ingestion artifact--: {ingestion_artifact}")
    v=DataValidation(data_ingestion_artifact=ingestion_artifact,data_validation_config=c.get_data_validation_config())
    t=DataTransformation(data_ingestion_artifact=ingestion_artifact,
                        data_validation_artifact=v.initiate_data_validation(),
                        data_transformation_config=c.get_data_transformation_config())
    tf=t.initiate_data_transformation()
    print(t.data_validation_artifact)
    print(tf)
    tr=ModelTrainer(data_transformation_artifact=tf,model_trainer_config=c.get_model_trainer_config())
    print(tr.initiate_model_trainer())
    




main()