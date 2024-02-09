from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from interfaces.Games import Games

router = APIRouter()

@router.get("/api/data/gamelist")
async def gameList() -> JSONResponse:
        return JSONResponse(Games.gameNames())