from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from interfaces.Games import Games

from methods.monster import loadMonsterList, getMonster, getRelatives, monsterOfTheDay

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
        return JSONResponse({"status": 2, "message": "Failed to get selected monster"})
    relatives = getRelatives(monster, monster_list)
    return JSONResponse([relative.model_dump(mode="json") for relative in relatives])


@router.post("/api/data/hint")
async def hint(game_selection: Games, seed: str, hint_num: int) -> JSONResponse:
    monster_list = loadMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list, seed)
    if hint_num not in (1, 2):
        return JSONResponse({"status": 2, "message": "Invalid hint number"})

    if hint_num == 1:
        return JSONResponse({"hint": motd.alias.strip()})

    if hint_num == 2:
        return JSONResponse({"hint": motd.description.strip()})
