from fastapi import FastAPI, Depends
import uvicorn
from search import search_router
from JWTToken import TokenValidation
from BaseHTTPExeption import http_exeption_handler, BaseHTTPExeption
from auth import auth_router
from user_account import user_account_router



app = FastAPI(exception_handlers = {
        BaseHTTPExeption : http_exeption_handler
    },
    dependencies = [Depends(TokenValidation.weak_check_access_token)]
)

app.include_router(search_router)
app.include_router(auth_router)
app.include_router(user_account_router)



if __name__ == '__main__':
    print(BaseHTTPExeption._all_responses_schemas)
    uvicorn.run(app, host = '127.0.0.1', port = 8000)