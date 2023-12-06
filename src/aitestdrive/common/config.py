import logging
import os
from typing import Any

from pydantic import BaseModel, ValidationError

from aitestdrive.common import constants

log = logging.getLogger(__name__)

additional_env_var_mappings = [
    ('PORT', 'LISTEN_PORT'),
    ('GOOGLE_CLOUD_PROJECT', 'GCP_PROJECT'),
]


class Config(BaseModel, frozen=True):
    listen_port: int = 8000
    gcp_project: str

    @staticmethod
    def from_env_dict(source_env_dict: dict[str, Any]) -> 'Config':
        lower_case_dict = {key.lower(): value for key, value in source_env_dict.items()}
        try:
            res = Config(**lower_case_dict)
        except ValidationError as ve:
            # extracting only some error details to hide potentially sensitive input
            raise ValueError(str(ve.errors(include_url=False, include_context=False, include_input=False))) from None
        # noinspection PyTypeChecker
        return res


def load_config():
    env_dict = {}

    # env file
    env_file_path = constants.ENV_FILE_PATH
    if env_file_path and os.path.exists(env_file_path):
        logging.info("Loading config from .env file...")
        from aitestdrive.common.dotenv import dotenv_values
        env_dict.update(dotenv_values(env_file_path))

    # env vars
    logging.info("Loading environment variables...")
    env_dict.update(os.environ)

    # additionally mapped env vars
    for source, target in additional_env_var_mappings:
        if source in env_dict:
            env_dict[target] = env_dict[source]

    return Config.from_env_dict(env_dict)


def load_and_export_config():
    global config

    logging.info("Loading config.")
    config = load_config()


config: Config

load_and_export_config()
