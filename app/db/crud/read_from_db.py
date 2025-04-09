from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_engine
from app.db.models import SettingGeneral, SettingDeveloper, SettingView
from finance_tracker_shared.schemas import SettingGeneralRead, SettingDeveloperRead, SettingViewRead

def get_all_settings_from_db_by_category() -> dict:
    engine = get_engine()
    with Session(engine) as session:
        general_settings = session.execute(select(SettingGeneral)).scalars().all()
        developer_settings = session.execute(select(SettingDeveloper)).scalars().all()
        view_settings = session.execute(select(SettingView)).scalars().all()

    engine.dispose()

    results_dict = {
        'general': {},
        'developer': {},
        'view': {}
    }

    for setting in general_settings:
        setting_dict = SettingGeneralRead.model_validate(setting).model_dump()
        results_dict['general'][setting.id] = setting_dict

    for setting in developer_settings:
        setting_dict = SettingDeveloperRead.model_validate(setting).model_dump()
        results_dict['developer'][setting.id] = setting_dict
    
    for setting in view_settings:
        setting_dict = SettingViewRead.model_validate(setting).model_dump()
        results_dict['view'][setting.id] = setting_dict
    
    return results_dict

def get_setting_by_category_and_key_from_db(category: str, key: str) -> dict:
    if category not in ["general", "developer", "view"]:
        raise ValueError("Invalid category. Must be one of: 'general', 'developer', 'view'.")

    engine = get_engine()
    with Session(engine) as session:
        try:
            if category == "general":
                query_result = session.execute(select(SettingGeneral).where(SettingGeneral.key == key)).scalars().first()
                setting_dict = SettingGeneralRead.model_validate(query_result).model_dump()
            elif category == "developer":
                query_result = session.execute(select(SettingDeveloper).where(SettingDeveloper.key == key)).scalars().first()
                setting_dict = SettingDeveloperRead.model_validate(query_result).model_dump()
            elif category == "view":
                query_result = session.execute(select(SettingView).where(SettingView.key == key)).scalars().first()
                setting_dict = SettingViewRead.model_validate(query_result).model_dump()
        except Exception as e:
            raise ValueError(f"Error retrieving setting: {e}")
    engine.dispose()

    return setting_dict
