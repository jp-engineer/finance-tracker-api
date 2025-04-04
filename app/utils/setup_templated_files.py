import os

import logging
logger = logging.getLogger(__name__)

def setup_templates(template_settings_path: str, user_setting_path: str) -> None:
    def setup_user_settings_yml():
        if not os.path.exists(user_setting_path):
            if not os.path.exists(template_settings_path):
                logger.error(f"Template file {template_settings_path} does not exist.")
                raise FileNotFoundError(f"Template file {template_settings_path} does not exist.")
            
            logger.info(f"user-settings.yml does not exist. Copying template settings from {template_settings_path} to {user_setting_path}")
            with open(template_settings_path, 'r') as template_file:
                template_content = template_file.read()
            with open(user_setting_path, 'w') as user_settings_file:
                user_settings_file.write(template_content)
    
    setup_user_settings_yml()
