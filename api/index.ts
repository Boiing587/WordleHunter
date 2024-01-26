import express from 'express'
import { JsonDB, Config } from 'node-json-db'
import Monster from './interfaces/monster'
import Monsters from './interfaces/monsters'

const db = new JsonDB(new Config('./data/monsters', true, true, '/'))

function generateMonsterOfTheDay(monsterList: Monsters): void {
  let monsters = Object.keys(monsterList)
  let randomMonster: Monster["name"] = monsters[ monsters.length * Math.random() << 0 ]
  console.log(randomMonster)
  console.log(monsterList.monster)
}

let monsterList: Monsters | null = null
db.getObject<Monsters>("/")
  .then((value: Monsters) => {
    monsterList = value
    console.info("Monster list successfully loaded.")
    generateMonsterOfTheDay(monsterList)
  })
  .catch(() => {
    console.error("Failed to load monster list.")
  })



// const newMonster: Monster = {
//   "species": "Flying wyvern",
//   "subspecies": "Rare species",
//   "generation": "Gen 4",
//   "game": "Monster Hunter 4",
//   "statuses": ["Blast"],
//   "weaknesses": ["Water", "Ice"]
// }

// db.push("/molten tigrex", newMonster)

const app = express()
const port = process.env.PORT || 3000

app.post('/guess', (req, res) => {
  res.send({"type": {"name": "dwagon", "closity": "meh"}, "home": "earf"})
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})