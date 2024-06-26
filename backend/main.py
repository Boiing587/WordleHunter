#!/usr/bin/env python3
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import data, guess

app = FastAPI()

routers = [
    data,
    guess
]

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost',
                                  'http://localhost:5173',
                                  'https://polite-cliff-095e41a03.4.azurestaticapps.net',
                                  'https://polite-cliff-095e41a03.4.azurestaticapps.net/',
                                  'https://polite-cliff-095e41a03.4.azurestaticapps.net/play',
                                  'https://wordlehunter.dev',
                                  'https://wordlehunter.dev/',
                                  'https://wordlehunter.dev/play',
                                  'https://www.wordlehunter.dev',
                                  'https://www.wordlehunter.dev/',
                                  'https://www.wordlehunter.dev/play'],
                   allow_methods=['GET', 'POST'])

for router in routers:
    app.include_router(router.router)

@app.get('/api/health')
async def health():
    return JSONResponse({'status': '0', 'message': 'ok'})

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=5000, reload=True, log_level='info')
