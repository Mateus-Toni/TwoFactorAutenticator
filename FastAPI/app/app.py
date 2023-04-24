from fastapi import APIRouter, FastAPI, status
from fastapi.responses import JSONResponse

from routes import user_routes, auth_routes


app = FastAPI()

@app.get('/', tags=['Main - Health Check'])
def  health_check():

    return JSONResponse(content={'msg': 'im ready'},
                        status_code=status.HTTP_200_OK)

app.include_router(user_routes.router, prefix='/user', tags=['User'])
app.include_router(auth_routes.router, prefix='/auth', tags=['Autenticação'])

