import yaml
from pydantic import ValidationError
from app.schemas.setting import SettingBase
from app.schemas.enums import SettingCategoryEnum
from app.utils.setup_templated_files import setup_templates

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
    except ValidationError as e:
        logger.warning(f"Invalid setting [{category}.{key}] = {value}: {e}")
        return False

def load_merged_settings(user_settings_path: str ="app/user/user-settings.yml",
                         default_settings_path: str ="app/defaults/default-settings.yml",
                         load_templates: bool = False,
                         templates_dir: str ="app/templates"):
    def read_yaml(path):
        try:
            data = yaml.safe_load(open(path,  "r", encoding='utf-8'))
            return data
        except FileNotFoundError:
            logger.error(f"File {path} not found. Returning empty dictionary.")
            return {}

    if load_templates:
        setup_templates(user_settings_path, templates_dir)

    user = read_yaml(user_settings_path)
    default = read_yaml(default_settings_path)
    merged = {}

    for category, keys in default.items():
        merged[category] = {}
        for key, default_val in keys.items():
            user_val = user.get(category, {}).get(key, None)

            if user_val is not None:
                try:
                    SettingBase(
                        category=SettingCategoryEnum(category),
                        key=key,
                        value=str(user_val)
                    )
                    merged[category][key] = user_val
                except ValidationError as e:
                    logger.warning(f"Invalid setting [{category}.{key}] = {user_val}: {e}")
                    merged[category][key] = default_val
            else:
                merged[category][key] = default_val

    logging.debug(f"Merged and validated settings: {merged}")
    return merged

def update_all_user_settings(user_settings_path: str ="app/user/user-settings.yml", settings: dict = None) -> dict:
    for category, keys in settings.items():
        for key, value in keys.items():
            if not validate_setting(category, key, value):
                raise ValueError(f"Invalid setting: {category}.{key} = {value}")

    with open(user_settings_path,  "w", encoding='utf-8') as file:
        yaml.dump(settings, file, default_flow_style=False, allow_unicode=True)
