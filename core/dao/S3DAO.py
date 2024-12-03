import aioboto3
from core.models.s3 import admin_s3, user_s3, S3UserSettings, s3config
from core.services_and_endpoints import servicesurls



class S3DAO:
    
    @classmethod
    def get_resource(cls, client_credentials : S3UserSettings):
        
        def decorator(func):
            async def wrapper(cls_or_self : S3DAO | type[S3DAO] | None = None, *args, **kwargs):
                session = aioboto3.Session(
                                            aws_access_key_id = client_credentials.keys[0].access,
                                            aws_secret_access_key = client_credentials.keys[0].secret,
                                            region_name = s3config.REGION
                                        )
                async with session.resource('s3',
                                           use_ssl = False,
                                           endpoint_url = servicesurls.S3
                                        ) as client:
                    return await func(cls_or_self, client, *args, **kwargs)
                    
            
            return wrapper
        return decorator
    
    
    @classmethod
    def get_user_resource(cls):
        return cls.get_resource(user_s3)
    
    @classmethod
    def get_admin_resource(cls):
        return cls.get_resource(admin_s3)
    