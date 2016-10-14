import express from 'express'
import cors from 'cors'
import http from 'http'
import socket_io from 'socket.io'
import shortid from 'shortid'


const app = express()
const httpServer = http.Server(app)
const io = socket_io(httpServer)
app.use(cors())
users = []

/* ==================================
            Endpoints
================================== */
app.get('/history', (req, res) => {
  // TODO get history from redis
  const history = []
  res.send({history: history})
})

app.get('/history/clear', (req, res) => {
  // TODO: clear redis key
  res.send({data: null})
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
})

/* ==================================
        Start the server
================================== */
app.listen(13493, () => {
  console.log('App listening on port 13493')
})
