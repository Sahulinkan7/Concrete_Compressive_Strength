from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
from concrete_strength.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from concrete_strength.entity.config_entity import DataValidationConfig
import pandas as pd
from concrete_strength.util.util import read_yaml_file,write_yaml_file
from concrete_strength.constant import *
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                    data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_file_path=self.data_validation_config.schema_file_path
            self.schema_config=read_yaml_file(self.schema_file_path)
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    @staticmethod
    def read_dataframe(file_path:str)->pd.DataFrame:
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise ConcreteException(e,sys) from e 

    def validate_number_of_columns(self,data_frame:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config[DATASET_SCHEMA_COLUMNS_KEY])
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"Data Frame has columns : {len(data_frame.columns)}")
            if number_of_columns==len(data_frame.columns):
                return True
            return False
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def is_numerical_columns_exist(self,data_frame:pd.DataFrame)->bool:
        try:
            numerical_columns=self.schema_config[DATASET_SCHEMA_NUMERICAL_COLUMNS_KEY]
            dataframe_columns=data_frame.columns

            is_numerical_columns_present=True
            missing_numerical_columns=[]

            for schema_num_column in numerical_columns:
                if schema_num_column not in dataframe_columns:
                    is_numerical_columns_present=False
                    missing_numerical_columns.append(schema_num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return is_numerical_columns_present
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dict=ks_2samp(d1,d2)
                if is_same_dict.pvalue>=threshold:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dict.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path=self.data_validation_config.report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,data=report)
            return drift_report_file_path,status
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message=""
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_data_frame=DataValidation.read_dataframe(train_file_path)
            test_data_frame=DataValidation.read_dataframe(test_file_path)

            status=self.validate_number_of_columns(data_frame=train_data_frame)
            if not status:
                error_message=f"Train data frame : {train_data_frame} does not contains all columns\n"
            status=self.validate_number_of_columns(data_frame=test_data_frame)
            if not status:
                error_message=f"Test data frame : {test_data_frame} does not contains all columns\n"

            status=self.is_numerical_columns_exist(data_frame=train_data_frame)
            if not status:
                error_message=f"train dataframe: {train_data_frame} does not contain all numerical columns"
            status=self.is_numerical_columns_exist(data_frame=test_data_frame)
            if not status:
                error_message=f"test data frame : {test_data_frame} does not contail all numerical columns"
            
            if len(error_message)>0:
                raise Exception(error_message)
            
            report_file_path,status=self.detect_dataset_drift(base_df=train_data_frame,current_df=test_data_frame)

            data_validation_artifact=DataValidationArtifact(schema_file_path=self.schema_file_path,
                                                            report_file_path=report_file_path,
                                                            is_validated=True,
                                                            message=f"Data validation done successfully")

            logging.info(f"Data validation artifact : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise ConcreteException(e,sys) from e

    