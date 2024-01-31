from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from methods.motd import monsterOfTheDay
from methods.monsterList import loadMonsterList

from interfaces.GameSelection import GameSelection

router = APIRouter()

@router.get("/api/guess")
async def guess(game_selection: GameSelection):
    monster_list = loadMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list)
    return JSONResponse(motd)