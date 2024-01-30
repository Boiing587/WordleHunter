#!/usr/bin/env python3
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routers import guess

app = FastAPI()

routers = [
    guess
]

for router in routers:
    app.include_router(router.router)

@app.get('/health')
async def health():
    return JSONResponse({'status': '0', 'message': 'ok'})

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5000, reload=True, log_level='info')