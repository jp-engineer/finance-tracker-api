import os
import json
import yaml
from datetime import date
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)

def read_yaml_file(file_path: str) -> dict:
    logger.debug(f"Reading YAML file: {file_path}")
    data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    else:
        logger.warning(f"File not found: {file_path}. Returning empty dictionary.")
    return data

def read_json_file(file_path: str) -> dict:
    logger.debug(f"Reading JSON file: {file_path}")
    data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        logger.warning(f"File not found: {file_path}. Returning empty dictionary.")
    return data

def load_settings_dict() -> dict:
    def deep_merge_dicts(defaults: dict, overrides: dict) -> dict:
        logger.debug(f"Deep merging dictionaries: {defaults} with {overrides}")
        result = {}
        for key, value in defaults.items():
            if key in overrides:
                if isinstance(value, dict) and isinstance(overrides[key], dict):
                    result[key] = deep_merge_dicts(value, overrides[key])
                else:
                    result[key] = overrides[key]
            else:
                result[key] = value
        logger.debug(f"Result of deep merge: {result}")

        return result

    default_settings_file = os.path.join(APP_CFG['DEFAULT_SETTINGS_DIR'], "default_user_settings.yml")
    user_data_dict = read_yaml_file(APP_CFG["SETTINGS_FILE"])
    default_data_dict = read_yaml_file(default_settings_file)

    cleaned_user_data_dict = {}
    for category, keys in user_data_dict.items():
        for key, value in keys.items():
            if value is None and key != "start_date":
                logger.debug(f"Removed empty value for {category}.{key}")
                continue

            if category not in cleaned_user_data_dict:
                cleaned_user_data_dict[category] = {}

            if key == "start_date" and value is None:
                logger.debug(f"start_date is None, setting to today")
                cleaned_user_data_dict[category][key] = date.today().strftime("%Y-%m-%d")
            else:
                cleaned_user_data_dict[category][key] = value

    for category, subdict in cleaned_user_data_dict.items():
        if category not in default_data_dict:
            raise ValueError(f"Category {category} not found in default settings.")
        for key in subdict:
            if key not in default_data_dict[category]:
                raise ValueError(f"Key {key} in {category} not found in default settings.")

    merged_data_dict = deep_merge_dicts(default_data_dict, cleaned_user_data_dict)

    if merged_data_dict.get('developer', {}).get('start_date') is None:
        merged_data_dict['developer']['start_date'] = date.today().strftime("%Y-%m-%d")
        logger.debug(f"Set start_date to today: {merged_data_dict['developer']['start_date']}")

    logger.debug(f"Merged settings: {merged_data_dict}")

    return merged_data_dict

# def convert_dict_of_settings_by_category(settings_dict: dict) -> dict:
#     logger.debug(f"Converting dictionary of settings by category: {settings_dict}")
#     converted_dict = {}

#     for category, settings_list in settings_dict.items():
#         for setting in settings_list:
#             if isinstance(setting, dict):
#                 key = setting.get("key")
#                 value = setting.get("value")
#                 converted_dict[key] = value

#     return converted_dict
