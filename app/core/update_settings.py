from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import ValidationError

from finance_tracker_shared.schemas import SettingGeneralUpdate, SettingDeveloperUpdate, SettingViewUpdate

from app.db.models import SettingGeneral, SettingDeveloper, SettingView
from app.db.database import get_engine
from app.core.helpers import read_yaml_file, write_yaml_file
from app.config import APP_CFG

import logging
logger = logging.getLogger(__name__)


def update_settings_in_db_from_dict(settings_dict: dict) -> None:
    engine = get_engine()

    with Session(engine) as session:
        for category, settings in settings_dict.items():
            if category == "general":
                for key, value in settings.items():

                    existing = session.query(SettingGeneral).filter_by(key=key).first()
                    if existing:
                        existing.value = value
                    else:
                        new_setting = SettingGeneral(key=key, value=value)
                        session.add(new_setting)

            elif category == "developer":
                for key, value in settings.items():
                    
                    existing = session.query(SettingDeveloper).filter_by(key=key).first()
                    if existing:
                        existing.value = value
                    else:
                        new_setting = SettingDeveloper(key=key, value=value)
                        session.add(new_setting)

            elif category == "view":
                for key, value in settings.items():
                    
                    existing = session.query(SettingView).filter_by(key=key).first()
                    if existing:
                        existing.value = value
                    else:
                        new_setting = SettingView(key=key, value=value)
                        session.add(new_setting)

        session.commit()
        engine.dispose()


def update_settings_in_file_from_dict(settings_dict: dict) -> None:
    existing_settings = read_yaml_file(APP_CFG["SETTINGS_FILE"])

    for category, settings in settings_dict.items():
        if category in existing_settings:
            existing_settings[category].update(settings)
        else:
            existing_settings[category] = settings
    
    write_yaml_file(APP_CFG["SETTINGS_FILE"], existing_settings)


def update_all_settings_from_dict(settings_dict: dict) -> None:
    input_lists = {
        "general": settings_dict.get("general", []),
        "developer": settings_dict.get("developer", []),
        "view": settings_dict.get("view", [])
    }

    input_dict = {
        "general": {},
        "developer": {},
        "view": {}
    }

    for category, settings_list in input_lists.items():
        for setting in settings_list:
            result = {setting["key"]: setting["value"]}
            input_dict[category].update(result)

    for category, settings in input_dict.items():
        if category == "general":
            for key, value in settings.items():

                try:
                    validated = SettingGeneralUpdate.model_validate({
                        "key": key,
                        "value": value
                    })
                    normalized_value = validated.value
                except ValidationError as e:
                    raise ValueError(f"Validation error: {e}")
                
        elif category == "developer":
            for key, value in settings.items():

                try:
                    validated = SettingDeveloperUpdate.model_validate({
                        "key": key,
                        "value": value
                    })
                    normalized_value = validated.value
                except ValidationError as e:
                    raise ValueError(f"Validation error: {e}")
                
        elif category == "view":
            for key, value in settings.items():

                try:
                    validated = SettingViewUpdate.model_validate({
                        "key": key,
                        "value": value
                    })
                    normalized_value = validated.value
                except ValidationError as e:
                    raise ValueError(f"Validation error: {e}")            

        input_dict[category][key] = normalized_value
    
    update_settings_in_file_from_dict(input_dict)
    update_settings_in_db_from_dict(input_dict)

    result_dict = {
        "success": True,
        "message": "Settings updated successfully."
    }

    return result_dict


def update_setting_by_category_and_key(category: str, key: str, value: str) -> None:
    input_dict = {
        category: {
            key: value
        }
    }

    update_settings_in_file_from_dict(input_dict)
    update_settings_in_db_from_dict(input_dict)

    result_dict = {
        "success": True,
        "message": f"Setting '{key}' in category '{category}' updated successfully."
    }
    
    return result_dict