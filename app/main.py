from fastapi import FastAPI
import uvicorn
from search.router import router as search_router


app = FastAPI()

app.include_router(search_router)


if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)