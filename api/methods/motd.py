import random

from datetime import datetime

from methods.monsterList import loadMonsterList

from interfaces.Generations import Generations
from interfaces.Monster import Monster

def monsterOfTheDay(generations: Generations) -> Monster:
    monsterList = loadMonsterList(generations)
    monsterNames = [monster['name'] for monster in monsterList]
    seed = datetime.today().strftime("%d/%m/%Y")
    random.seed(seed)
    random.shuffle(monsterNames)
    monster_of_the_day = random.choice(monsterNames)
    return [monster for monster in monsterList if monster['name'] == monster_of_the_day][0]
