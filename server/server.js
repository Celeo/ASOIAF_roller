import express from 'express'
import cors from 'cors'
import request from 'request'
import moment from 'moment'


const app = express()
app.use(cors())

app.get('/', (req, res) => {
  res.send('Hello world')
})

/* ==================================
        Start the server
================================== */
app.listen(13493, () => {
  console.log('App listening on port 13493')
})
