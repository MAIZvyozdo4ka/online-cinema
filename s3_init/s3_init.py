from core.dao import S3DAO
from asyncio import run
from boto3.resources.base import ServiceResource
from core.models.s3 import s3config
import os


class InitS3:
    
    @classmethod
    @S3DAO.get_admin_resource()
    async def full_init(cls, client : ServiceResource) -> None:
        await client.create_bucket(Bucket = s3config.MOVIE_BUCKET_NAME, ACL = s3config.MOVIE_BUCKET_ACL)
        movie_bucket = await client.Bucket(s3config.MOVIE_BUCKET_NAME)
        with open('s3_init/movie_mp4/movie.csv', 'r+') as init_file:
            for file in init_file:
                id, file_path = file.replace('"', '').removesuffix('\n').split(',', 1)
                with open(file_path, 'rb') as read_file:
                    await movie_bucket.upload_fileobj(read_file, f'{s3config.MOVIE_BUCKET_NAME}_{id}.mp4')
        
        
        
        
        
run(InitS3.full_init())