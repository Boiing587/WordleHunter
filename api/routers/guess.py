from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from methods.compare import compareGuess
from methods.monster import loadSelectedMonsterList, monsterOfTheDay

from interfaces.Guess import Guess
from interfaces.Games import GameSelection

router = APIRouter()

@router.get("/api/guess")
async def guess(data: Guess) -> JSONResponse:
    guess = data.guess
    game_selection = data.games
    monster_list = loadSelectedMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list)
    if not (comparison := compareGuess(guess, motd)):
        return JSONResponse({'status': 404, 'message': 'monster not found'})
    return comparison

@router.get("/api/cheat")
async def cheat(game_selection: GameSelection) -> JSONResponse:
    monster_list = loadSelectedMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list)
    print(type(motd))
    return JSONResponse(motd.__dict__)