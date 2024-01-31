from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from methods.motd import monsterOfTheDay

from interfaces.GameSelection import GameSelection

router = APIRouter()

@router.get("/api/guess")
async def guess(game_selection: GameSelection):
    if not game_selection:
        return JSONResponse({'status': 2, 'message': 'Request body missing.'})
    return JSONResponse(monsterOfTheDay(game_selection))