from .schemas import MovieOut
from core.models.postgres import MovieDB
from .errors import MovieNotFoundError, MovieVideoNotFoundError
from core.dao import PostgresDAO, AsyncSession, S3DAO
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from core.models.s3 import s3config
from core.schemas import MovieID
from fastapi.responses import StreamingResponse
import aioboto3
from core.models.s3 import admin_s3, s3config
from core.services_and_endpoints import servicesurls





class MovieDAO(PostgresDAO):
        
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_movie_by_id(cls,
                              session : AsyncSession,
                              movie_id : MovieID
                            ) -> MovieOut:
        query_for_select_movie_with_links = select(MovieDB).options(selectinload(MovieDB.link)).where(MovieDB.id == movie_id)
        movie = await session.scalar(query_for_select_movie_with_links)
        
        if movie is None:
            raise MovieNotFoundError
        
        return MovieOut.model_validate(movie)
    
    
class S3Stream(StreamingResponse):
    def __init__(
            self,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            movie_id : MovieID | None = None
    ) -> None:
        super(S3Stream, self).__init__(None, status_code, headers, media_type, None)
        self.movie_id = movie_id

    async def stream_response(self, send) -> None:
        await send(
            {
                'type': 'http.response.start',
                'status': self.status_code,
                'headers': self.raw_headers,
            }
        )

        session = aioboto3.Session(
                                        aws_access_key_id = admin_s3.keys[0].access,
                                        aws_secret_access_key = admin_s3.keys[0].secret,
                                        region_name = s3config.REGION
                                    )
        async with session.client('s3',
                                   use_ssl = False,
                                   endpoint_url = servicesurls.S3
                                ) as client:
            
            movie = await client.get_object(Bucket=s3config.MOVIE_BUCKET_NAME, Key=f'{s3config.MOVIE_BUCKET_NAME}_{self.movie_id}.mp4')
            async for chunk in movie['Body']:
                if not isinstance(chunk, bytes):
                    chunk = chunk.encode(self.charset)
                await send({'type': 'http.response.body', 'body': chunk, 'more_body': True})
        await send({'type': 'http.response.body', 'body': b'', 'more_body': False})

   
    
    
    
    
class MovieS3DAO(S3DAO):

    
    @classmethod
    @S3DAO.get_admin_resource()
    async def get_movie_video(cls, client, movie_id : MovieID) -> StreamingResponse:
        movie_obj = await client.ObjectSummary(s3config.MOVIE_BUCKET_NAME, f'{s3config.MOVIE_BUCKET_NAME}_{movie_id}.mp4')
        try:
            await movie_obj.get()
        except Exception:
            raise MovieVideoNotFoundError
        return S3Stream(status_code = 200, movie_id = movie_id)
            
    
    
    
