import os
import yaml

import logging
logger = logging.getLogger(__name__)

def read_yaml_file(file_path):
    logger.debug(f"Reading YAML file: {file_path}")
    data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    else:
        logger.warning(f"File not found: {file_path}. Returning empty dictionary.")
    return data
