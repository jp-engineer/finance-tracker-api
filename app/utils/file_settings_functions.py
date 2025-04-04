from datetime import date
import yaml
from pydantic import ValidationError
from app.schemas.setting import SettingBase
from app.schemas.enums import SettingCategoryEnum

import logging
logger = logging.getLogger(__name__)

def validate_setting(category: str, key: str, value: str) -> bool:
    try:
        SettingBase(
            category=SettingCategoryEnum(category),
            key=key,
            value=value
        )
        return True
    except (ValidationError, ValueError) as e:
        logger.warning(f"Invalid setting [{category}.{key}] = {value}: {e}")
        return False

def update_all_user_settings(user_settings_path: str ="app/user/user-settings.yml", settings: dict = None) -> dict:
    for category, keys in settings.items():
        for key, value in keys.items():
            if value is None and key == "start_date":
                value = date.today().strftime("%Y-%m-%d")
            if not validate_setting(category, key, value):
                raise ValueError(f"Invalid setting: {category}.{key} = {value}")

    with open(user_settings_path,  "w", encoding='utf-8') as file:
        yaml.dump(settings, file, default_flow_style=False, allow_unicode=True)
