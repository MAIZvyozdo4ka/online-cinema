import aioboto3
from core.models.s3 import admin_s3, user_s3, S3UserSettings, s3config
from core.services_and_endpoints import servicesurls




admin_session = aioboto3.Session(
                        aws_access_key_id = admin_s3.keys[0].access,
                        aws_secret_access_key = admin_s3.keys[0].secret,
                        region_name = s3config.REGION
                    )