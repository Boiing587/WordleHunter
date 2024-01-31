import random

from datetime import datetime

from interfaces.Monster import Monster

def monsterOfTheDay(monster_list: list[Monster]) -> Monster:
    monsterNames = [monster['name'] for monster in monster_list]
    seed = datetime.today().strftime("%d/%m/%Y")
    random.seed(seed)
    random.shuffle(monsterNames)
    monster_of_the_day = random.choice(monsterNames)
    return [monster for monster in monster_list if monster['name'] == monster_of_the_day][0]
