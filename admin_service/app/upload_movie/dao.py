from core.dao import S3DAO
from boto3.resources.base import ServiceResource
from core.models.s3 import s3config
from fastapi import UploadFile
from core.schemas import MovieID
from .errors import IncorrectFileTypeError




class MovieS3DAO(S3DAO):
    
    
    @classmethod
    @S3DAO.get_admin_resource()
    async def upload_movie(cls, client : ServiceResource, movie_file : UploadFile, movie_id : MovieID) -> None:
        if movie_file.headers['content-type'] != 'video/mp4':
            raise IncorrectFileTypeError
        
        movie_bucket = await client.Bucket(s3config.MOVIE_BUCKET_NAME)
        await movie_bucket.upload_fileobj(movie_file, f'{s3config.MOVIE_BUCKET_NAME}_{movie_id}.mp4')
        
    
    @classmethod
    @S3DAO.get_admin_resource()
    async def delete_movie(cls, client : ServiceResource, movie_id : MovieID) -> None:
        movie_bucket = await client.Bucket(s3config.MOVIE_BUCKET_NAME)
        await movie_bucket.delete_objects(
                                   Delete = {
                                            'Objects': [
                                                {
                                                    'Key': f'{s3config.MOVIE_BUCKET_NAME}_{movie_id}.mp4'
                                                }
                                            ]
                                        }
                                   )
