import os
from datetime import date
import yaml
from pydantic import ValidationError
from app.config import APP_CFG
from finance_tracker_shared.schemas import SettingGeneralBase

import logging
logger = logging.getLogger(__name__)

def validate_setting(category: str, key: str, value: str) -> bool:
    # try:
    #     SettingBase(
    #         category=SettingCategoryEnum(category),
    #         key=key,
    #         value=value
    #     )

    #     return True
    
    # except (ValidationError, ValueError) as e:
    #     logger.warning(f"Invalid setting [{category}.{key}] = {value}: {e}")

    #     return False
    return True

def update_all_user_settings_in_file(settings: dict = None) -> dict:
    for category, keys in settings.items():
        for key, value in keys.items():
            if value is None and key == "start_date":
                value = date.today().strftime("%Y-%m-%d")
            if not validate_setting(category, key, value):
                raise ValueError(f"Invalid setting: {category}.{key} = {value}")

    logger.debug(f"Updating settings file: {APP_CFG["SETTINGS_FILE"]} with settings: {settings}")
    with open(APP_CFG["SETTINGS_FILE"],  "w", encoding='utf-8') as file:
        yaml.dump(settings, file, default_flow_style=False, allow_unicode=True)

def setup_user_settings_file() -> None:
    user_setting_path = APP_CFG['SETTINGS_FILE']
    template_settings_path = os.path.join(APP_CFG['TEMPLATE_SETTINGS_DIR'], 'user_settings.yml')

    if not os.path.exists(user_setting_path):
        if not os.path.exists(template_settings_path):
            logger.error(f"Template file {template_settings_path} does not exist.")
            raise FileNotFoundError(f"Template file {template_settings_path} does not exist.")
        
        logger.debug(f"user_settings.yml does not exist. Copying template settings from {template_settings_path} to {user_setting_path}")
        with open(template_settings_path, 'r') as template_file:
            template_content = template_file.read()
        with open(user_setting_path, 'w') as user_settings_file:
            user_settings_file.write(template_content)
