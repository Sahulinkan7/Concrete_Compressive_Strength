from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
from concrete_strength.constant import *
from concrete_strength.entity.config_entity import DataTransformationConfig
from concrete_strength.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact,DataTransformationArtifact
from concrete_strength.util.util import *
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class DataTransformation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                    data_validation_artifact:DataValidationArtifact,
                    data_transformation_config:DataTransformationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise ConcreteException(e,sys) from e

    @staticmethod
    def read_dataframe(file_path:str)->pd.DataFrame:
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def get_data_transformer_object(self):
        try:
            preprocessor=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])
            return preprocessor

        except Exception as e:
            raise ConcreteException(e,sys) from e

    def initiate_data_transformation(self):
        try:
            train_df=DataTransformation.read_dataframe(file_path=self.data_ingestion_artifact.train_file_path)
            test_df=DataTransformation.read_dataframe(file_path=self.data_ingestion_artifact.test_file_path)

            preprocessor=self.get_data_transformer_object()

            schema=read_yaml_file(file_path=self.data_validation_artifact.schema_file_path)
            target_column=schema[DATASET_SCHEMA_TARGET_COLUMN_KEY]

            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]

            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=test_df[target_column]

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_arr=preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test_arr=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_feature_train_arr,np.array(input_feature_train_df)]
            test_arr=np.c_[transformed_input_feature_test_arr,np.array(input_feature_test_df)]

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            train_file_name=os.path.basename(self.data_ingestion_artifact.train_file_path).replace(".xls",".npz")
            test_file_name=os.path.basename(self.data_ingestion_artifact.test_file_path).replace(".xls",".npz")

            transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)

            logging.info(f"Saving transformed train and test array")
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            preprocessing_object_file_path=self.data_transformation_config.preprocessed_object_file_path
            logging.info(f"Saving preprocessing object ")
            save_object(file_path=preprocessing_object_file_path,obj=preprocessor_object)

            data_transformation_artifact=DataTransformationArtifact(
                                                                    transformed_train_file_path=transformed_train_file_path,
                                                                    transformed_test_file_path=transformed_test_file_path,
                                                                    preprocessed_object_file_path=preprocessing_object_file_path,
                                                                    is_transformed=True,
                                                                    message=f" Data Transformed Successfully")
            logging.info(f"Data Transformation Artifact : {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ConcreteException(e,sys) from e