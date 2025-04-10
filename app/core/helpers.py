import os
import json
from datetime import date

import yaml

from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)


SETTINGS_DICT = {
    "general": [
        "country_code",
        "default_currency",
        "default_currency_symbol"
    ],
    "developer": [
        "start_date"
    ],
    "view": [
        "user_name",
        "week_starts_on",
        "date_format"
    ]
}


def check_e2e_mode() -> bool:
    e2e = False
    if APP_CFG["MODE"] == "e2e_testing":
        e2e = True
        
    return e2e


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


def write_yaml_file(file_path: str, data: dict) -> None:
    if not os.path.exists(os.path.dirname(file_path)):
        raise FileNotFoundError(f"Directory does not exist: {os.path.dirname(file_path)}")
    
    if data is None or data == {}:
        raise ValueError("Data to write cannot be None or empty dictionary.")

    logger.debug(f"Writing YAML file: {file_path} with data: {data}")
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)


def load_user_settings_dict() -> dict:
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
    

    def verify_user_settings_dict(user_data: dict) -> dict:
        verified_user_data_dict = {}
        for category, keys in user_data.items():
            for key, value in keys.items():
                if value is None and key != "start_date":
                    logger.debug(f"Removed empty value for {category}.{key}")
                    continue

                if category not in verified_user_data_dict:
                    verified_user_data_dict[category] = {}

                if key == "start_date" and value is None:
                    logger.debug(f"start_date is None, setting to today")
                    verified_user_data_dict[category][key] = date.today().strftime("%Y-%m-%d")

                else:
                    verified_user_data_dict[category][key] = value

        for category, subdict in verified_user_data_dict.items():
            if category not in default_data_dict:
                raise ValueError(f"Category {category} not found in default settings.")
            
            for key in subdict:
                if key not in default_data_dict[category]:
                    raise ValueError(f"Key {key} in {category} not found in default settings.")
                
        return verified_user_data_dict


    default_settings_file = os.path.join(APP_CFG['DEFAULT_SETTINGS_DIR'], "default_user_settings.yml")
    user_data_dict = read_yaml_file(APP_CFG["SETTINGS_FILE"])
    default_data_dict = read_yaml_file(default_settings_file)

    verified_user_data_dict = verify_user_settings_dict(user_data_dict)

    merged_data_dict = deep_merge_dicts(default_data_dict, verified_user_data_dict)

    if merged_data_dict.get('developer', {}).get('start_date') is None:
        merged_data_dict['developer']['start_date'] = date.today().strftime("%Y-%m-%d")
        logger.debug(f"Set start_date to today: {merged_data_dict['developer']['start_date']}")

    logger.debug(f"Merged settings: {merged_data_dict}")

    return merged_data_dict


def check_settings_dict_for_missing_keys(input_settings_dict: dict) -> None:
    for category, setting_list in SETTINGS_DICT.items():
        for setting in setting_list:
            if category not in input_settings_dict:
                raise ValueError(f"Missing category: {category} in settings dictionary.")
            if setting not in input_settings_dict[category]:
                raise ValueError(f"Missing setting: {setting} in category: {category}.")        