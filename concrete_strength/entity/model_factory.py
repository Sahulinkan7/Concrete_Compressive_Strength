from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
import yaml
import importlib
from concrete_strength.constant import *
from collections import namedtuple
from typing import List
import numpy as np
from sklearn.metrics import r2_score,mean_squared_error


InitializedModelDetail=namedtuple("InitializedModelDetail",
["model_serial_number","model","param_grid_search","model_name"])

GridSearchedBestDetailofModel=namedtuple("GridSearchedBestDetailofModel",
["model_serial_number","model","best_model","best_parameters","best_score"])

BestModel=namedtuple("BestModel",
["model_serial_number","model","best_model","best_parameters","best_score"])

MetricInfoArtifact=namedtuple("MetricInfoArtifact",
["model_name","model_object","train_rmse","test_rmse","train_accuracy","test_accuracy","model_accuracy","index_number"])
def evaluate_regression_model(model_list:list,x_train:np.array,y_train:np.array,x_test:np.array,y_test:np.array,base_accuracy:float=0.6):
    """
    This function compares multiple regresiion model and returns best model   
    
    params:
    model_list: List of model
    x_train: training dataset input feature
    y_train: training dataset target feature
    x_test: testing dataset input feature
    y_test: testing dataset target feature

    return: it returns a namedtuple MetricInfoArtifact
    MetricInfoArtifact=namedtuple("MetricInfoArtifact",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                "test_accuracy", "model_accuracy", "index_number"])

    """
    try:
        index_number=0
        for model in model_list:
            model_name=str(model)
            logging.info(f"{'##'*30} started evaluating model [{type(model).__name__}]{'##'*30}")

            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            train_acc=r2_score(y_train,y_train_pred)
            test_acc=r2_score(y_test,y_test_pred)

            train_rmse=np.sqrt(mean_squared_error(y_train,y_train_pred))
            test_rmse=np.sqrt(mean_squared_error(y_test,y_test_pred))

            model_accuracy=(2*(train_acc*test_acc))/(train_acc+test_acc)
            diff_train_test_acc=abs(train_acc-test_acc)

            logging.info(f"{'##'*30} Score {'##'*30}")
            logging.info(f"Train Score\t\t Test Score\t\t Average Score")
            logging.info(f"{train_acc}\t\t{test_acc}\t\t{model_accuracy}")

            logging.info(f"{'##'*30} Loss {'##'*30}")
            logging.info(f"Diff test train accuracy : [{diff_train_test_acc}]")
            logging.info(f"Train root mean squared error: [{train_rmse}]")
            logging.info(f"Test root mean squared error : [{test_rmse}]")

            if model_accuracy>=base_accuracy and diff_train_test_acc<0.5:
                base_accuracy=model_accuracy
                metric_info_artifact=MetricInfoArtifact(model_name=model_name,
                                                        model_object=model,
                                                        train_rmse=train_rmse,
                                                        test_rmse=test_rmse,
                                                        train_accuracy=train_acc,
                                                        test_accuracy=test_acc,
                                                        model_accuracy=model_accuracy,
                                                        index_number=index_number)
                logging.info(f"Acceptable model found {metric_info_artifact}")
            index_number+=1
        if metric_info_artifact is None:
            logging.info(f"No model found with better accuracy than base accuracy")
        return metric_info_artifact
        
    except Exception as e:
        raise ConcreteException(e,sys) from e


class ModelFactory:
    def __init__(self,model_config_path:str=None):
        try:
            self.config:dict=ModelFactory.read_params(model_config_path)
            self.grid_search_cv_module: str=self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_cv_class: str=self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_cv_property: dict=self.config[GRID_SEARCH_KEY][PARAM_KEY]
            self.models_initialization_config:dict=dict(self.config[MODEL_SELECTION_KEY])

            self.initialized_models_list=None
            self.grid_searched_best_model_list=None

        except Exception as e:
            raise ConcreteException(e,sys) from e

    @staticmethod
    def read_params(file_path:str)->dict:
        try:
            with open(file_path) as yaml_file:
                config:dict=yaml.safe_load(yaml_file)
            return config
        except Exception as e:
            raise ConcreteException(e,sys) from e

    @staticmethod
    def get_model_name(module_name:str,class_name:str):
        try:
            module=importlib.import_module(module_name)
            logging.info(f"Executing command : from {module} import {class_name}")
            model_ref_name=getattr(module,class_name)
            return model_ref_name
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    @staticmethod
    def update_model_property(instance_ref:object,property_data:dict):
        try:
            if not isinstance(property_data,dict):
                raise Exception("Property_data is required in dictionary format")
            print(property_data)
            for key,val in property_data.items():
                logging.info(f"Executing : {str(instance_ref)}.{key}={val}")
                setattr(instance_ref,key,val)
            return instance_ref
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def get_initialized_model_list(self)->List[InitializedModelDetail]:
        try:
            initialized_models_list=[]
            for model_serial_number in self.models_initialization_config.keys():

                model_initialization_config=self.models_initialization_config[model_serial_number]
                model_obj_ref=ModelFactory.get_model_name(module_name=model_initialization_config[MODULE_KEY],
                                                    class_name=model_initialization_config[CLASS_KEY])
                model=model_obj_ref()

                if PARAM_KEY in model_initialization_config:
                    model_obj_property_data=dict(model_initialization_config[PARAM_KEY])
                    model=ModelFactory.update_model_property(instance_ref=model,property_data=model_obj_property_data)

                param_grid_search=model_initialization_config[SEARCH_PARAM_GRID_KEY]
                model_name=f"{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}"

                model_initialization_config=InitializedModelDetail(model_serial_number=model_serial_number,
                                                                    model=model,
                                                                    param_grid_search=param_grid_search,
                                                                    model_name=model_name)
                initialized_models_list.append(model_initialization_config)
            self.initialized_models_list=initialized_models_list
            return self.initialized_models_list

        except Exception as e:
            raise ConcreteException(e,sys) from e

    def execute_grid_search_operation(self,initialized_model:InitializedModelDetail,
                                        input_feature,
                                        output_feature):
        try:
            grid_search_cv_ref=ModelFactory.get_model_name(module_name=self.grid_search_cv_module,
                                                        class_name=self.grid_search_cv_class)

            grid_search_cv=grid_search_cv_ref(estimator=initialized_model.model,param_grid=initialized_model.param_grid_search)
            grid_search_cv=ModelFactory.update_model_property(grid_search_cv,self.grid_search_cv_property)

            message=f'{"##"*30} f"Training {type(initialized_model.model).__name__} started."{"##"*30}'
            logging.info(message)

            grid_search_cv.fit(input_feature,output_feature)
            message=f'{"##"*30} f"Training {type(initialized_model.model).__name__} completed."{"##"*30}'

            grid_searched_best_details_of_model=GridSearchedBestDetailofModel(model_serial_number=initialized_model.model_serial_number,
                                                                            model=initialized_model.model,
                                                                            best_model=grid_search_cv.best_estimator_,
                                                                            best_parameters=grid_search_cv.best_params_,
                                                                            best_score=grid_search_cv.best_score_)
            return grid_searched_best_details_of_model
        except Exception as e:
            raise ConcreteException(e,sys) from e
    def initiate_best_parameter_search_for_initialized_model(self,initialized_model:InitializedModelDetail,
                                                                input_feature,
                                                                output_feature):
        try:
            return self.execute_grid_search_operation(initialized_model=initialized_model,
                                                        input_feature=input_feature,
                                                        output_feature=output_feature)
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def initiate_best_parameter_search_for_initialized_models(self,
                                                                initialized_model_list:List[InitializedModelDetail],
                                                                input_feature,
                                                                output_feature)->List[GridSearchedBestDetailofModel]:
        try:
            self.grid_searched_best_model_list=[]
            for initialized_model in initialized_model_list:
                grid_searched_best_model=self.initiate_best_parameter_search_for_initialized_model(
                                            initialized_model=initialized_model,
                                            input_feature=input_feature,
                                            output_feature=output_feature)
                self.grid_searched_best_model_list.append(grid_searched_best_model)
            return self.grid_searched_best_model_list
        except Exception as e:
            raise ConcreteException(e,sys) from e

    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list:List[GridSearchedBestDetailofModel],
                                                            base_accuracy=0.6)->BestModel:                                                       
        try:
            best_model=None
            for grid_searched_best_model in grid_searched_best_model_list:
                if base_accuracy<grid_searched_best_model.best_score:
                    logging.info(f"Acceptable model found: {grid_searched_best_model}")
                    base_accuracy=grid_searched_best_model.best_score

                    best_model=grid_searched_best_model
            if not best_model:
                raise Exception(f"None of the model has base accuracy {base_accuracy}")
            logging.info(f"best model: {best_model}")
            return best_model
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def get_best_model(self,x,y,base_accuracy=0.6)->BestModel:
        try:
            logging.info(f"Started Initializeng model from model config file")
            initialized_model_list=self.get_initialized_model_list()
            logging.info(f"Initialized model list {initialized_model_list}")

            grid_searched_best_model_list=self.initiate_best_parameter_search_for_initialized_models(
                                                initialized_model_list=initialized_model_list,
                                                input_feature=x,
                                                output_feature=y)
            
            return ModelFactory.get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list=grid_searched_best_model_list,base_accuracy=base_accuracy)
        except Exception as e:
            raise ConcreteException(e,sys) from e