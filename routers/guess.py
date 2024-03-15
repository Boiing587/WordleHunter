from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from methods.compare import compareGuess
from methods.monster import monsterOfTheDay, getMonster, loadMonsterList

from interfaces.Guess import Guess
from interfaces.Games import Games

router = APIRouter()

@router.post("/api/guess")
async def guess(data: Guess) -> JSONResponse:
    if not (guess := getMonster(data.guess)):
        return JSONResponse({'status': 2, 'message': "Failed to get guessed monster. This shouldn't be possible unless you made a request to this endpoint yourself"})
    game_selection = data.games
    monster_list = loadMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list)
    if not (comparison := compareGuess(guess, motd)):
        return JSONResponse({'status': 404, 'message': 'monster not found'})
    return JSONResponse({'guess': guess.model_dump(mode="json"), 'result': comparison.model_dump(mode="json")})

@router.post("/api/cheat")
async def cheat(game_selection: Games) -> JSONResponse:
    monster_list = loadMonsterList(game_selection)
    motd = monsterOfTheDay(monster_list)
    return JSONResponse(motd.model_dump(mode="json"))
