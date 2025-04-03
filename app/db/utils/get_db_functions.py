from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_engine
from app.db.models.setting import Setting

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
