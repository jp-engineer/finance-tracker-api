from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.setting import Setting
from app.db.database import get_engine

def get_all_settings_from_db() -> dict:
    engine = get_engine()
    with Session(engine) as session:
        result = session.execute(select(Setting)).all()

        if not result:
            settings_dict_by_category = {}

        settings_by_category = defaultdict(dict)
        for row in result:
            setting = row[0]
            settings_by_category[setting.category][setting.key] = setting.value

        settings_dict_by_category = dict(settings_by_category)

    engine.dispose()
    return settings_dict_by_category

def get_setting_from_db(category: str, key: str) -> dict:
    all_settings = get_all_settings_from_db()
    if category not in all_settings:
        return None
    if key not in all_settings[category]:
        return None
    results = {
        "key": key,
        "category": category,
        "value": all_settings[category][key]
    }
    return results
