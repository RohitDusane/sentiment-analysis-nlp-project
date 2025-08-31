
import os, sys
import logging
from datetime import datetime

# Create Logs folder
LOG_Dir = 'logs'
os.makedirs(LOG_Dir, exist_ok=True)

# Log File Name
LOG_FILE_NAME = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"
LOG_PATH = os.path.join(LOG_Dir, LOG_FILE_NAME)

# Handlers
handlers = [
    logging.StreamHandler(sys.stdout),
    logging.FileHandler(str(LOG_PATH), encoding='utf-8')
]

# Basic Config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y_%H:%M:%S",
    handlers=handlers
)


# # Testing
# if __name__=='__main__':
#     logging.info("The Logsis created!!!!!!")

