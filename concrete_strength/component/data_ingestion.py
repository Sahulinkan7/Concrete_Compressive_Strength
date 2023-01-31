from concrete_strength.exception import ConcreteException
from concrete_strength.logger import logging
import os,sys
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from concrete_strength.entity.config_entity import DataIngestionConfig
from concrete_strength.entity.artifact_entity import DataIngestionArtifact



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'##'*30} Data Ingestion Log started {'##'*30}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise ConcreteException(e,sys) from e
    
    def download_dataset(self)->str:
        try:
            download_url=self.data_ingestion_config.dataset_download_url
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir,exist_ok=True)
            concrete_file_name=os.path.basename(download_url)
            dataset_file_path=os.path.join(raw_data_dir,concrete_file_name)

            logging.info(f"dataset downloading started")
            urllib.request.urlretrieve(download_url,dataset_file_path)
            logging.info(f"file : [{dataset_file_path}] has been downloaded succesfully")

            return dataset_file_path
        except Exception as e:
            raise ConcreteException(e,sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir

            file_name=os.listdir(raw_data_dir)[0]

            concrete_file_path=os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file  [{concrete_file_path}]")
            concrete_data_frame=pd.read_excel(concrete_file_path)
            
            concrete_data_frame['cement_cat']=pd.cut(concrete_data_frame['Cement (component 1)(kg in a m^3 mixture)'],
                                                    bins=[100,190,280,370,460,np.inf],
                                                    labels=[1,2,3,4,5])
            
            logging.info(f"Splitting data into train and test ")
            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.15,random_state=30)

            for train_index,test_index in split.split(concrete_data_frame,concrete_data_frame['cement_cat']):
                strat_train_set=concrete_data_frame.loc[train_index].drop(["cement_cat"],axis=1)
                strat_test_set=concrete_data_frame.loc[test_index].drop(["cement_cat"],axis=1)

            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting train dataset into file : [{train_file_path}]")
                strat_train_set.to_excel(train_file_path,index=False)
            
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting test dataset into file : [{test_file_path}]")
                strat_test_set.to_excel(test_file_path,index=False)

            data_ingestion_artifact=DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message="Data Ingestion Completed successfully")
            
            logging.info(f" data ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise ConcreteException(e,sys) from e
 
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.download_dataset()
            return self.split_data_as_train_test()
        except Exception as e:
            raise ConcreteException(e,sys) from e