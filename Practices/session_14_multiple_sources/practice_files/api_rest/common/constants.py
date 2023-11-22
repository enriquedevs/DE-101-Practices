import os
from pathlib import Path
from enum import Enum

FOLDER_SEPARATOR = '/'
FILE_SEPARATOR = '_'
EXTENSION_SEPARATOR = '.'

BASE_DIR = Path(os.path.dirname(__file__)).parent.parent

BASE_FOLDER = f"{BASE_DIR}/generated_data"

class Format(Enum):
  CSV = 'csv'
  JSON = 'json'
