import os
from datetime import date, datetime

from sqlalchemy.orm import Session
from pydantic import ValidationError

import finance_tracker_shared.schemas as schemas

import app.db.models as models
from app.db.database import get_engine
from app.core.setup_user_settings import update_all_user_settings_in_file
from app.core.helpers import read_json_file, load_user_settings_dict, check_settings_dict_for_missing_keys
from app.db.utils.delete_db import check_for_db_reset
from app.config import APP_CFG


import logging
logger = logging.getLogger(__name__)
    

def setup_database() -> None:
    check_for_db_reset()
    new_db = init_db()
    if new_db:
        if APP_CFG["DB_SEED_FILE"]:
            if not os.path.exists(APP_CFG["DB_SEED_FILE"]):
                raise FileNotFoundError(f"Seed file not found: {APP_CFG['DB_SEED_FILE']}")
            logger.debug(f"Seeding database with file: {APP_CFG['DB_SEED_FILE']}")
            seed_dict = read_json_file(APP_CFG["DB_SEED_FILE"])
            seed_db_with_data(seed_dict)

        else:
            logger.debug("No seed file provided, seeding settings.")
            settings_dict = load_user_settings_dict()
            seed_setting_tables(settings_dict)
            update_all_user_settings_in_file(settings_dict)
    logger.info(f"Database initialized at {APP_CFG['DB_PATH']}")


def init_db(engine: object=None) -> None:
    new_db = False
    if engine is None:
        engine = get_engine()
        dispose_after = True
    else:
        dispose_after = False

    if not os.path.exists(APP_CFG["DB_PATH"]):
        new_db = True
        logger.debug(f"Database file does not exist. Creating: {APP_CFG['DB_PATH']}.")
        models.Base.metadata.create_all(bind=engine)

    if dispose_after:
        engine.dispose()

    return new_db


def seed_db_with_data(data_dict: dict, engine: object=None) -> None:
    def convert_date_strings_in_dict_to_date(data_dict: dict) -> dict:
        for model, model_data in data_dict.items():
            if model == "ScheduledTransaction":
                for entry in model_data:
                    if "scheduled_date" in entry:
                        entry["scheduled_date"] = datetime.strptime(
                            entry["scheduled_date"], "%Y-%m-%d"
                        ).date()
            elif model == "TransactionAll":
                for entry in model_data:
                    if "date" in entry:
                        entry["date"] = datetime.strptime(
                            entry["date"], "%Y-%m-%d"
                        ).date()

        return data_dict
    
    settings_input_dict = {"general": {}, "developer": {}, "view": {}}

    settings_general_list = data_dict.get("SettingGeneral", [])
    for setting in settings_general_list:
        settings_input_dict["general"][setting["key"]] = setting["value"]
    settings_developer_list = data_dict.get("SettingDeveloper", [])
    for setting in settings_developer_list:
        settings_input_dict["developer"][setting["key"]] = setting["value"]
    settings_view_list = data_dict.get("SettingView", [])
    for setting in settings_view_list:
        settings_input_dict["view"][setting["key"]] = setting["value"]
    
    check_settings_dict_for_missing_keys(settings_input_dict)
    
    data_dict_converted = convert_date_strings_in_dict_to_date(data_dict)
    if engine is None:
        engine = get_engine()
    logger.debug(f"Seeding DB at {APP_CFG['DB_PATH']}")

    setting_developer_list = data_dict_converted["SettingDeveloper"]
    valid = True
    for setting_dict in setting_developer_list:
        if setting_dict.get("key") == "start_date":
            if setting_dict.get("value") is None:
                valid = True
                break
    if not valid:
        raise ValueError("start_date is None in SettingDeveloper. Please provide a valid date.")

    settings_file_dict = {"general": {}, "developer": {}, "view": {}}
    with Session(engine) as session:
        for model_name, model_data in data_dict_converted.items():
            model_class = getattr(models, model_name, None)
            if model_class is None:
                raise ValueError(f"Model {model_name} not found in app.db.models")

            for item in model_data:
                try:
                    if model_name == "AccountAll":
                        validated = schemas.AccountAllCreate(**item)

                    elif model_name == "AccountCredit":
                        validated = schemas.AccountCreditCreate(**item)
                    
                    elif model_name == "AccountDebit":
                        validated = schemas.AccountDebitCreate(**item)

                    elif model_name == "AccountIndependent":
                        validated = schemas.AccountIndependentCreate(**item)

                    elif model_name == "Folio":
                        validated = schemas.FolioCreate(**item)
                    
                    elif model_name == "RecurringTransaction":
                        validated = schemas.RecurringTransactionCreate(**item)

                    elif model_name == "ScheduledTransaction":
                        validated = schemas.ScheduledTransactionCreate(**item)
                    
                    elif model_name == "SettingGeneral":
                        validated = schemas.SettingGeneralCreate(**item)
                        settings_file_dict['general'][item['key']] = validated.value
                    
                    elif model_name == "SettingDeveloper":
                        validated = schemas.SettingDeveloperCreate(**item)
                        settings_file_dict['developer'][item['key']] = validated.value

                    elif model_name == "SettingView":
                        validated = schemas.SettingViewCreate(**item)
                        settings_file_dict['view'][item['key']] = validated.value

                    elif model_name == "TransactionAll":
                        validated = schemas.TransactionAllCreate(**item)
                    
                    elif model_name == "TransactionExpense":
                        validated = schemas.TransactionExpenseCreate(**item)
                    
                    elif model_name == "TransactionPayment":
                        validated = schemas.TransactionPaymentCreate(**item)

                    elif model_name == "TransactionTransfer":
                        validated = schemas.TransactionTransferCreate(**item)

                except ValidationError as e:
                    raise ValueError(f"Error validating {model_name} with data {item}: {e}")

                try:
                    existing = session.query(model_class).filter_by(**validated.model_dump()).first()
                    if not existing:
                        db_model = model_class(**validated.model_dump())
                        session.add(db_model)
                except Exception as e:
                    raise ValueError(f"Error inserting {model_name} with data {validated}: {e}")


        session.commit()
        engine.dispose()

    update_all_user_settings_in_file(settings_file_dict)


def seed_setting_tables(settings_dict: dict, engine: object=None) -> None:
    if engine is None:
        engine = get_engine()
    logger.debug(f"DB at {APP_CFG['DB_PATH']} with settings: {settings_dict}")

    check_settings_dict_for_missing_keys(settings_dict)

    with Session(engine) as session:
        for category, key_value in settings_dict.items():
            if category == "general":
                for key, value in key_value.items():
                    try:
                        validated = schemas.SettingGeneralCreate(key=key, value=value)
                        existing = session.query(models.SettingGeneral).filter_by(key=key).first()
                        if not existing:
                            db_setting = models.SettingGeneral(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")
            
            elif category == "developer":
                for key, value in key_value.items():
                    try:
                        if value is None and key == "start_date":
                            value = date.today().strftime("%Y-%m-%d")
                            logger.debug(f"Setting start_date to today, ie: {value}")

                        validated = schemas.SettingDeveloperCreate(key=key, value=value)
                        existing = session.query(models.SettingDeveloper).filter_by(key=key).first()
                        if not existing:
                            db_setting = models.SettingDeveloper(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")
 
            elif category == "view":
                for key, value in key_value.items():
                    try:
                        validated = schemas.SettingViewCreate(key=key, value=value)
                        existing = session.query(models.SettingView).filter_by(key=key).first()
                        if not existing:
                            db_setting = models.SettingView(**validated.model_dump())
                            session.add(db_setting)
                            logger.debug(f"Inserted: {key} with value: {value} in category: {category}")
                    except ValidationError as e:
                        raise ValueError(f"Error inserting {key} in category {category}: {e}")

        session.commit()
        engine.dispose()


def re_init_db() -> None:
    if os.path.exists(APP_CFG['DB_PATH']):
        os.remove(APP_CFG['DB_PATH'])
        logger.info(f"Deleted database file: {APP_CFG['DB_PATH']}")

    init_db()