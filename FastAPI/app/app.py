from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from routes import auth
from routes import user

app = FastAPI()

@app.get('/', tags=['Health Check'])
def  health_check():  

    return JSONResponse(content={'msg': 'im ready'},
                        status_code=status.HTTP_200_OK)

app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(auth.router, prefix='/auth', tags=['Autenticação'])

