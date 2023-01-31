
from datetime import datetime
import os

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

ROOT_DIR=os.getcwd()
CURRENT_TIME_STAMP=get_current_time_stamp()
CONFIG_DIR="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)


#training related variables
TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY="pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR="artifact_dir"

#data ingestion related variables
DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_NAME_KEY="raw_data_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY="ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_NAME_KEY="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_NAME_KEY="ingested_test_dir"
DATA_INGESTION_ARTIFACT_DIR_NAME_KEY="data_ingestion"