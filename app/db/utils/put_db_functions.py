from sqlalchemy.orm import Session
from app.db.models.setting import Setting
from app.db.database import get_engine

def put_all_settings_to_db(settings: dict) -> None:
    engine = get_engine()
    with Session(engine) as session:
        for category, settings in settings.items():
            for key, value in settings.items():
                setting = session.query(Setting).filter_by(category=category, key=key).first()
                if setting:
                    setting.value = value
                else:
                    raise ValueError(f"Setting with category '{category}' and key '{key}' not found in the database.")

        session.commit()

    engine.dispose()
