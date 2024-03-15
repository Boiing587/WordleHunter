from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from interfaces.Games import Games

from methods.monster import loadMonsterList, getMonster, getRelatives

router = APIRouter()

@router.get("/api/data/gamelist")
async def gameList() -> JSONResponse:
    return JSONResponse(Games.gameNames())

@router.post("/api/data/monsters")
async def monsterList(game_selection: Games) -> JSONResponse:
    monster_list = loadMonsterList(game_selection)
    return JSONResponse([monster.model_dump(mode="json") for monster in monster_list])

@router.get("/api/data/relatives")
async def relativeMonsters(name: str) -> JSONResponse:
    monster_list = loadMonsterList()
    if not (monster := getMonster(name)):
        return JSONResponse({'status': 2, 'message': 'Failed to get selected monster'})
    relatives = getRelatives(monster, monster_list)
    return JSONResponse([relative.model_dump(mode="json") for relative in relatives])
