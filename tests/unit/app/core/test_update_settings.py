import pytest
import yaml

from app.config import APP_CFG

from app.core.update_settings import (
    update_settings_in_db_from_dict,
    update_settings_in_file_from_dict,
    update_all_settings_from_dict,
    update_setting_by_category_and_key
)


pytestmark = [
    pytest.mark.unit,
    pytest.mark.core
]


