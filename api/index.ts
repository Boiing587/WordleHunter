import express from 'express'
import { JsonDB, Config } from 'node-json-db'

const db = new JsonDB(new Config('./data/monsters', true, true, '/'))

const app = express()
const port = process.env.PORT || 3000

app.post('/guess', (req, res) => {
  res.send({"type": {"name": "dwagon", "closity": "meh"}, "home": "earf"})
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})