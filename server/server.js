import express from 'express'
import cors from 'cors'
import httplib from 'http'
import socket_io from 'socket.io'
import shortid from 'shortid'
import redislib from 'redis'
import config from '../config.js'


/* ==================================
            Setup
================================== */
const app = express()
const http = httplib.Server(app)
const io = socket_io(http)
const redis = redislib.createClient({
  host: config.redis.host,
  port: config.redis.port,
  db: config.redis.db,
  password: config.redis.password
})
app.use(cors())

let users = []

/* ==================================
            Endpoints
================================== */
app.get('/history', (req, res) => {
  // TODO get history from redis
  const history = []
  res.send({history: history})
})

app.get('/history/clear', (req, res) => {
  redis.del('history')
  res.send({history: []})
})

app.get('/users', (req, res) => {
  res.send({users: users})
})

/* ==================================
        Socket connections
================================== */
io.on('connection', (socket => {
  socket.id = shortid.generate()
  console.log('A user connected and was given the unique id ' + socket.id)

  socket.on('disconnect', () => {
    console.log(`A user disconnected, had the unique id ${socket.id}`
      + ` and username ${socket.username}`)
      const index = users.indexOf(socket.username)
    if (index > -1)
      users.splice(index, 1)
  })

  socket.on('setname', (msg) => {
    console.log(`Got ${msg} from client targeting 'setname'`)
    users.push(msg.name)
    socket.username = msg.name
  })

  socket.on('leave', (msg) => {
    console.log(`Got ${msg} from client targeting 'leave'`)
    const index = users.indexOf(socket.username)
    if (index > -1)
      users.splice(index, 1)
    socket.username = ''
    io.emit('users')
  })

  socket.on('roll_request', (msg) => {
    console.log(`Got ${msg} from client targeting 'roll_request'`)
    /*
    TODO:
      1. Generate the random numbers
      2. Calculate the steps of the roll and the final result
      3. Store in redis
      4. Broadcast the roll to all websocket clients
    */
  })
}))

/* ==================================
          Redis conection
================================== */
redis.on('connect', () => {
  console.log('Redis connection started')
})
redis.on('ready', () => {
  console.log('Redis connected')
})
redis.on('error', (err) => {
  console.log('A redis error occurred: ' + err)
})
redis.on('reconnected', (delay, attempt) => {
  console.log(`Redis attempting to reconnect, attempt ${attempt}`)
})
redis.on('end', () => {
  console.log('Redis disconnected')
})

/* ==================================
          Start the server
================================== */
app.listen(13493, () => {
  console.log('App listening on port 13493')
})
