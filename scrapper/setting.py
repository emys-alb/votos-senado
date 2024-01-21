import os
from dotenv import load_dotenv

load_dotenv()

FILE_NAME_SETTING = os.getenv("FILE_NAME")
INIT_DATE_SETTING = os.getenv("INIT_DATE")
FINISH_DATE_SETTING = os.getenv("FINISH_DATE")
