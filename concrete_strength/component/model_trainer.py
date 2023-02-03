from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
import numpy as np
import pandas as pd
import importlib
from typing import List
from concrete_strength.entity.config_entity import ModelTrainerConfig
from concrete_strength.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from concrete_strength.util.util import load_numpy_array_data,load_object,save_object
from concrete_strength.entity.model_factory import (ModelFactory,GridSearchedBestDetailofModel,
                                                    evaluate_regression_model,MetricInfoArtifact)
class ConcreteEstimatorModel:
    def __init__(self,preprocessing_object,trained_model_object):
        """
        Trained model 
        preprocessing_object: preprocessing object 
        trained_model : trained model
        
        """
        try:
            self.preprocessing_object=preprocessing_object
            self.trained_model_object=trained_model_object
        except Exception as e:
            raise ConcreteException(e,sys) from e
    def predict(self,x):
        """
        function takes raw inouts and tranforms input using preprocessing_object
        then predicts the output using those transformed data
        """
        try:
            transformed_feature=self.preprocessing_object.transform(x)
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise ConcreteException(e,sys) from e

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                    model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    def initiate_model_trainer(self):
        try:
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path=self.data_transformation_artifact.transformed_train_file_path
            train_array=load_numpy_array_data(file_path=transformed_train_file_path)

            logging.info(f"Loading transformed test dataset")
            transformed_test_file_path=self.data_transformation_artifact.transformed_test_file_path
            test_array=load_numpy_array_data(file_path=transformed_test_file_path)

            logging.info(f"Splitting training and testing input and target feature")
            x_train,y_train,x_test,y_test=train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]
            
            logging.info(f"Extracting model config file path")
            model_config_file_path=self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file : {model_config_file_path}")
            model_factory=ModelFactory(model_config_path=model_config_file_path)

            base_accuracy=self.model_trainer_config.base_accuracy
            logging.info(f"Expected Accuracy : {base_accuracy}")

            logging.info(f"Initiating operation model selection")
            best_model=model_factory.get_best_model(x=x_train,y=y_train,base_accuracy=base_accuracy)

            logging.info(f"Best Model found on training dataset {best_model}")

            logging.info(f"Extracting trained model list")
            grid_searched_best_model_list:List[GridSearchedBestDetailofModel]=model_factory.grid_searched_best_model_list

            model_list=[model.best_model for model in grid_searched_best_model_list]
            
            logging.info(f"Evaluating all trained model on training and testing dataset")
            metric_info:MetricInfoArtifact=evaluate_regression_model(model_list=model_list,x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,base_accuracy=base_accuracy)

            logging.info(f"Best model found on both training and testing dataset")

            preprocessing_obj=load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object=metric_info.model_object

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            concrete_model=ConcreteEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path : {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=concrete_model)

            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=trained_model_file_path,
                                                        train_rmse=metric_info.train_rmse,
                                                        test_rmse=metric_info.test_rmse,
                                                        train_accuracy=metric_info.train_accuracy,
                                                        test_accuracy=metric_info.test_accuracy,
                                                        model_accuracy=metric_info.model_accuracy,
                                                        is_trained=True,
                                                        message=f"Model Trained Successfully")
            
            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact
             
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'##'*30} Model Trainer log completed {'##'*30}")

    