import logging 
import logging.handlers
import os 
import WorkbenchBase

LOG_DIR = WorkbenchBase.LOGGER_PATH
WORKBENCH_NAME = WorkbenchBase.__title__

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(WORKBENCH_NAME)
logger.setLevel(logging.DEBUG)

# Console + file handler
handler = logging.handlers.RotatingFileHandler(os.path.join(LOG_DIR, f"{WORKBENCH_NAME}.log"), maxBytes=1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)