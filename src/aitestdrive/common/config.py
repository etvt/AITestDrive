import logging
import os
from typing import Any

from pydantic import BaseModel, ValidationError, Field

from aitestdrive.common import constants
from aitestdrive.common.default_config import get_google_cloud_project, DEFAULT_PORT

log = logging.getLogger(__name__)

additional_env_var_mappings = [
    ('PORT', 'LISTEN_PORT'),
    ('GCLOUD_PROJECT', 'GOOGLE_CLOUD_PROJECT'),
]


class Config(BaseModel, frozen=True):
    listen_port: int = DEFAULT_PORT
    google_cloud_project: str = Field(default_factory=get_google_cloud_project)
    document_bucket: str
    qdrant_url: str
    qdrant_api_key: str

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
        dotenv_dict = dotenv_values(env_file_path)
        env_dict.update(dotenv_dict)
        os.environ.update(dotenv_dict)

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
