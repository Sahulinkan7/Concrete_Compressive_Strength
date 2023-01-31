import os,sys
import logging
from concrete_strength.constant import *



from datetime import datetime

LOG_DIR="Concrete_Strength_Log"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)
logging.basicConfig(filename=LOG_FILE_PATH,level=logging.INFO,
                    filemode="w",
                    format='[%(asctime)s] %(name)s - %(levelname)s -%(message)s')