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
app.use(cors({
  origin: 'http://localhost:8080',
  credentials: true
}))

let users = []

/* ==================================
            Endpoints
================================== */
app.get('/history', (req, res) => {
  const history = []
  redis.lrange('history', 0, -1, (err, lastNode) => {
    for (let item of lastNode)
      history.push(JSON.parse(item))
    res.json({history: history})
  })
})

app.get('/history/clear', (req, res) => {
  redis.del('history')
  res.json({history: []})
})

app.get('/users', (req, res) => {
  res.json({users: users})
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

/*
Leftover Python
  @socketio.on('roll_request')
  def handle_roll_request(message):
      try:
          ability = int(message.get('ability') or 2)
          bonus = int(message.get('bonus') or 0)
          static = int(message.get('static') or 0)
          total = 0
          rolls = []
          keep_rolls = []
          all_rolls = []
          for _ in range(ability + bonus):
              rolls.append(random.randint(1, 6))
          all_rolls = list(map(str, rolls))
          for _ in range(ability):
              keep_rolls.append(rolls.pop(rolls.index(max(rolls))))
          total = sum(keep_rolls)
          keep_rolls = map(str, keep_rolls)
          h = None
          if static:
              h = History(name(), '{}, {}'.format(ability, bonus), '{} -> {} -> {} -> {}'.format(
                  ','.join(all_rolls) + '+' + str(static),
                  ','.join(keep_rolls) + '+' + str(static),
                  str(total) + '+' + str(static),
                  str(total + static)))
          else:
              h = History(name(), '{}, {}'.format(ability, bonus), '{} -> {} -> {}'.format(','.join(all_rolls), ','.join(keep_rolls), total + static))
          redis.lpush('history', h.to_json())
          emit('roll_event', {}, broadcast=True)
      except Exception as e:
          print(e)


  class History:

      def __init__(self, name, dice, result):
          self.name = name
          self.dice = dice
          self.result = result
          self.date = arrow.utcnow().to('US/Pacific').strftime('%I:%M:%S %p')

      def to_json(self):
          return json.dumps({
              'name': self.name,
              'dice': self.dice,
              'result': self.result,
              'date': self.date
          })

      @staticmethod
      def from_json(s):
          j = json.loads(s.decode('utf-8'))
          return History(j['name'], j['dice'], j['result'], j['date'])

*/

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
