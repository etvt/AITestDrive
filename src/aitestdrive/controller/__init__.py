from google.cloud import aiplatform

from aitestdrive.common.config import config

aiplatform.init(project=config.google_cloud_project)
