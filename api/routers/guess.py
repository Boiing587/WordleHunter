from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from methods.motd import monsterOfTheDay

from interfaces.Generations import Generations

router = APIRouter()

@router.get("/api/guess")
async def guess(generations: Generations):
    return JSONResponse(monsterOfTheDay(generations))