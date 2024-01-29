import express from 'express'
import { monsterList } from '../data/monsterList'
import getMonsterOfTheDay from '../methods/motd'

export const router = express.Router()

router.get('/guess', (req, res) => {
  let monsterOfTheDay = getMonsterOfTheDay()
  if (!monsterOfTheDay) {
    res.send({"ok": false, "msg": "sorry, shit seems to have hit the fan. please try again later."})
    return
  }
  res.send(`Today's monster is ${monsterOfTheDay.name}`)
})

router.post('/guess', (req, res) => {
  if (!monsterList) {
    res.send({"ok": false, "msg": "sorry, shit seems to have hit the fan. please try again later."})
    return
  }
  monsterList.filter(m => m.name == "guy")[0]
  res.send({"type": {"name": "dwagon", "closity": "meh"}, "home": "earf"})
})

