from concrete_strength.config.configuration import Configuration
from concrete_strength.util.util import read_yaml_file
from concrete_strength.constant import *
from concrete_strength.component.data_ingestion import DataIngestion
from concrete_strength.component.data_validation import DataValidation
from concrete_strength.component.data_transformation import DataTransformation
from concrete_strength.component.model_trainer import ModelTrainer
from concrete_strength.component.model_evaluation import ModelEvaluation
from concrete_strength.component.model_pusher import ModelPusher


def main():

    c=Configuration(config_file_path=r"config/config.yaml",current_time_stamp=CURRENT_TIME_STAMP)
    d=DataIngestion(data_ingestion_config=c.get_data_ingestion_config())
    ingestion_artifact=d.initiate_data_ingestion()
    print(f"--ingestion artifact--: {ingestion_artifact}")
    v=DataValidation(data_ingestion_artifact=ingestion_artifact,data_validation_config=c.get_data_validation_config())
    vart=v.initiate_data_validation()
    print(f"--validation artifact--{vart}")
    t=DataTransformation(data_ingestion_artifact=ingestion_artifact,
                        data_validation_artifact=vart,
                        data_transformation_config=c.get_data_transformation_config())
    tf=t.initiate_data_transformation()
    print(f"--data transformation artifact--{tf}")
    tr=ModelTrainer(data_transformation_artifact=tf,model_trainer_config=c.get_model_trainer_config())
    trart=tr.initiate_model_trainer()
    print(f"--model trainer artifact-- {trart}")

    ev=ModelEvaluation(model_evaluation_config=c.get_model_evaluation_config(),
                        data_ingestion_artifact=ingestion_artifact,
                        data_validation_artifact=vart,
                        model_trainer_artifact=trart)
    evart=ev.initiate_model_evaluation()
    print(f"--model evaluation artifact-- {evart}")
    
    mp=ModelPusher(model_evaluation_artifact=evart,model_pusher_config=c.get_model_pusher_config())
    mpart=mp.initiate_model_pusher()
    print(f"---Model Pusher Artifact ---{mpart}")
    




main()