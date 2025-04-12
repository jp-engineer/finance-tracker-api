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
            if settings:
                if category == "general":            
                    for key, value in settings.items():
                        existing = session.query(SettingGeneral).filter_by(key=key).first()
                        if existing:
                            existing.value = value
                        else:

                            raise ValueError(f"Setting '{key}' not found in the database.")

                elif category == "developer":
                    for key, value in settings.items():
                            existing = session.query(SettingDeveloper).filter_by(key=key).first()
                            if existing:
                                existing.value = value
                            else:

                                raise ValueError(f"Setting '{key}' not found in the database.")

                elif category == "view":
                    for key, value in settings.items():

                        if settings:
                            existing = session.query(SettingView).filter_by(key=key).first()
                            if existing:
                                existing.value = value
                            else:

                                raise ValueError(f"Setting '{key}' not found in the database.")
            
                else:

                    raise ValueError(f"Invalid category '{category}'. Valid categories are 'general', 'developer', and 'view'.")

        session.commit()
        engine.dispose()


def update_settings_in_file_from_dict(settings_dict: dict) -> None:
    existing_settings = read_yaml_file(APP_CFG["SETTINGS_FILE"])

    for category, settings in settings_dict.items():
        if category not in ["general", "developer", "view"]:

            raise ValueError(f"Invalid category '{category}'. Valid categories are 'general', 'developer', and 'view'.")

        for key, value in settings.items():
            if key not in existing_settings[category]:

                raise ValueError(f"Key '{key}' not found in the existing settings.")

            if category == "general":
                try:
                    input_settings = {
                        "key": key,
                        "value": value
                    }
                    validated = SettingGeneralUpdate.model_validate(input_settings)
                    value = validated.value

                except ValidationError as e:

                    raise ValueError(f"Validation error: {e}")
                
            elif category == "developer":
                try:
                    input_settings = {
                        "key": key,
                        "value": value
                    }
                    validated = SettingDeveloperUpdate.model_validate(input_settings)
                    value = validated.value

                except ValidationError as e:

                    raise ValueError(f"Validation error: {e}")
                
            elif category == "view":
                try:
                    input_settings = {
                        "key": key,
                        "value": value
                    }
                    validated = SettingViewUpdate.model_validate(input_settings)

                except ValidationError as e:

                    raise ValueError(f"Validation error: {e}")
            
            existing_settings[category].update(settings)
    
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
            result = {setting['key'] : setting['value']}
            input_dict[category].update(result)

    if input_dict["general"] == {} and input_dict["developer"] == {} and input_dict["view"] == {}:

        raise ValueError("No settings provided to update.")

    for category, settings_dict in input_dict.items():
        if settings_dict:
            if category == "general":
                for key, value in settings_dict.items():

                    try:
                        validated = SettingGeneralUpdate.model_validate({
                            "key": key,
                            "value": value
                        })
                        normalized_value = validated.value

                    except ValidationError as e:

                        raise ValueError(f"Validation error: {e}")
                    
            elif category == "developer":
                for key, value in settings_dict.items():

                    try:
                        validated = SettingDeveloperUpdate.model_validate({
                            "key": key,
                            "value": value
                        })
                        normalized_value = validated.value

                    except ValidationError as e:

                        raise ValueError(f"Validation error: {e}")
                    
            elif category == "view":
                for key, value in settings_dict.items():

                    try:
                        validated = SettingViewUpdate.model_validate({
                            "key": key,
                            "value": value
                        })
                        normalized_value = validated.value

                    except ValidationError as e:

                        raise ValueError(f"Validation error: {e}")

            else:
                
                raise ValueError(f"Invalid category '{category}'. Valid categories are 'general', 'developer', and 'view'.")      

            input_dict[category][key] = normalized_value
    
    update_settings_in_file_from_dict(input_dict)
    update_settings_in_db_from_dict(input_dict)


def update_setting_by_category_and_key(category: str, key: str, value: str) -> None:
    input_dict = {
        category: {
            key: value
        }
    }

    update_settings_in_file_from_dict(input_dict)
    update_settings_in_db_from_dict(input_dict)