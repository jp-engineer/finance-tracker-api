from fastapi import APIRouter
from pydantic import ValidationError
from finance_tracker_shared.schemas import APIResponse
from finance_tracker_shared.schemas import SettingAllUpdatePayload, SettingGeneralUpdate, SettingDeveloperUpdate, SettingViewUpdate
from app.core.update_settings import update_all_settings_from_dict, update_setting_by_category_and_key
#from app.core.helpers import convert_dict_of_settings_by_category
#from app.db.crud.update_in_db import update_setting_in_db_by_key, update_settings_in_db_from_dict

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/settings")

@router.put("/put-all-settings", response_model=APIResponse)
def put_all_settings(request: SettingAllUpdatePayload) -> APIResponse:
    logger.info("PUT /settings/put-all-settings")
    logger.debug(f"Received PUT request to update all settings: {request}")

    settings_dict = request.model_dump()
    result_dict = update_all_settings_from_dict(settings_dict)

    if result_dict['success']:
        logger.info("All settings updated successfully.")
    else:
        logger.error(f"Failed to update all settings: {result_dict['message']}")

    return result_dict

@router.put("/general/put-setting", response_model=APIResponse)
def put_general_setting(request: SettingGeneralUpdate, category="general") -> APIResponse:
    logger.info(f"PUT /settings/{category}/put-setting")

    try:
        validated = SettingGeneralUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")
    
    result_dict = update_setting_by_category_and_key(category, request.key, normalized_value)

    return result_dict

@router.put("/developer/put-setting", response_model=APIResponse)
def put_developer_setting(request: SettingDeveloperUpdate, category="developer") -> APIResponse:
    logger.info(f"PUT /settings/{category}/put-setting")

    try:
        validated = SettingGeneralUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value

    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")

    result_dict = update_setting_by_category_and_key(category, request.key, normalized_value)

    return result_dict

@router.put("/view/put-setting", response_model=APIResponse)
def put_view_setting(request: SettingViewUpdate, category="view") -> APIResponse:
    logger.info(f"PUT /settings/{category}/put-setting")

    try:
        validated = SettingGeneralUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value

    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")

    result_dict = update_setting_by_category_and_key(category, request.key, normalized_value)

    return result_dict
