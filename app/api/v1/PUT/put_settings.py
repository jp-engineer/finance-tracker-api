from fastapi import APIRouter
from pydantic import ValidationError

from finance_tracker_shared.schemas import (
    APIResponse, SettingAllUpdatePayload,
    SettingGeneralUpdate, SettingDeveloperUpdate, SettingViewUpdate
)

from app.core.update_settings import update_all_settings_from_dict, update_setting_by_category_and_key

import logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/settings")


@router.put("/put-all-settings", response_model=APIResponse)
def put_all_settings(request: SettingAllUpdatePayload) -> APIResponse:
    settings_dict = request.model_dump()

    result_dict = {
        "message": "Settings updated successfully",
        "data": True
    }
    logger.debug(f"Received settings_dict: {settings_dict}")

    return result_dict


@router.put("/general/put-setting", response_model=APIResponse)
def put_general_setting(request: SettingGeneralUpdate, category="general") -> APIResponse:
    try:
        validated = SettingGeneralUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value

    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")
    
    result_dict = {
        "message": "Setting updated successfully",
        "data": {}
    }

    update_setting_by_category_and_key(category, request.key, normalized_value)
    result_dict["data"] = {request.key: normalized_value}

    logger.debug(f"Updated setting: {request.key} with value: {normalized_value}")
    

    return result_dict


@router.put("/developer/put-setting", response_model=APIResponse)
def put_developer_setting(request: SettingDeveloperUpdate, category="developer") -> APIResponse:
    try:
        validated = SettingDeveloperUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value

    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")

    result_dict = {
        "message": "Setting updated successfully",
        "data": {}
    }
    
    update_setting_by_category_and_key(category, request.key, normalized_value)
    result_dict["data"] = {request.key: normalized_value}

    logger.debug(f"Updated setting: {request.key} with value: {normalized_value}")


    return result_dict


@router.put("/view/put-setting", response_model=APIResponse)
def put_view_setting(request: SettingViewUpdate, category="view") -> APIResponse:
    try:
        validated = SettingViewUpdate.model_validate({
            "key": request.key,
            "value": request.value
        })
        normalized_value = validated.value

    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")

    result_dict = {
        "message": "Setting updated successfully",
        "data": {}
    }
    
    update_setting_by_category_and_key(category, request.key, normalized_value)
    result_dict["data"] = {request.key: normalized_value}
    
    logger.debug(f"Updated setting: {request.key} with value: {normalized_value}")


    return result_dict