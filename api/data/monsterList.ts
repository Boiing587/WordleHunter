import Monster from "../interfaces/monster"
import { JsonDB, Config } from "node-json-db"

const db = new JsonDB(new Config('./data/monsters', true, true, '/'))

export var monsterList: Monster[] | null = null
db.getObject<Monster[]>('/')
  .then((value: Monster[]) => {
    monsterList = value
    console.info('Monster list successfully loaded.')
  })
  .catch(() => {
    console.error('Failed to load monster list.')
  })