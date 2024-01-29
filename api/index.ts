import express from 'express'
import { router as guess } from './routes/guess'

const app = express()
app.use('/', guess)

const port = process.env.PORT || 3000

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})