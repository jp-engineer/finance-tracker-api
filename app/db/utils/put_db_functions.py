from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_engine
from app.db.models.setting import Setting

def put_all_settings_to_db(input_settings: dict) -> None:
    engine = get_engine()
    with Session(engine) as session:
        for category, settings in input_settings.items():
            for key, value in settings.items():
                setting = session.query(Setting).filter_by(category=category, key=key).first()
                if setting:
                    setting.value = value
                else:
                    raise ValueError(f"Setting with category '{category}' and key '{key}' not found in the database.")

        session.commit()

    engine.dispose()
