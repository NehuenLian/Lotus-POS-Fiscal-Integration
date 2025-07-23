from pathlib import Path

from dotenv import set_key

import os
from src.utils.logger_config import business_logger


class SettingsManagement:
    def __init__(self):
        pass

    def update_db_url(self, db_url: str) -> None:
        env_path = Path(".env")  # or absolute path
        set_key(dotenv_path=env_path, key_to_set="DB_URL", value_to_set=db_url)
        os.environ["DB_URL"] = db_url
        
        business_logger.info(f"Database URL successfully updated to: {db_url}")
