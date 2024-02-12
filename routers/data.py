from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from interfaces.Games import Games

from methods.monster import loadMonsterList, getMonster, getRelatives

router = APIRouter()

@router.get("/api/data/gamelist")
async def gameList() -> JSONResponse:
        return JSONResponse(Games.gameNames())

@router.get("/api/data/relatives")
async def relativeMonsters(name: str) -> JSONResponse:
        monster_list = loadMonsterList()
        monster = getMonster(name)
        return JSONResponse(getRelatives(monster, monster_list))