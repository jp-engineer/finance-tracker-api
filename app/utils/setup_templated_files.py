import os
from app.utils.load_settings_from_files import USER_SETTINGS_PATH

import logging
logger = logging.getLogger(__name__)

TEMPLATES_DIR = "app/templates/"

def setup_templates():
    def setup_user_settings_yml():
        if not os.path.exists(USER_SETTINGS_PATH):
            template_settings_path = os.path.join(TEMPLATES_DIR, "user-settings.yml")
            if not os.path.exists(template_settings_path):
                logger.error(f"Template file {template_settings_path} does not exist.")
                raise FileNotFoundError(f"Template file {template_settings_path} does not exist.")
            
            logger.info(f"user-settings.yml does not exist. Copying template settings from {template_settings_path} to {USER_SETTINGS_PATH}")
            with open(template_settings_path, 'r') as template_file:
                template_content = template_file.read()
            with open(USER_SETTINGS_PATH, 'w') as user_settings_file:
                user_settings_file.write(template_content)
    
    setup_user_settings_yml()
