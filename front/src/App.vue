<template>
<div>
    <div class="row">
        <div class="col-md-12">
            <p id="error" v-if="!connected && hasConnected">Socket server is disconnected</p>
        </div>
    </div>
    <div class="row">
        <div class="col-md-9">
            <div class="panel panel-default">
                <div class="panel-body">
                    <div id="control" class="float-middle">
                        <div class="row">
                            <div class="col-sm-2 col-sm-offset-2">
                                <input class="form-control" v-model="ability" placeholder="Ability dice">
                            </div>
                            <div class="col-sm-2">
                                <input class="form-control" v-model="bonus" placeholder="Bonus dice">
                            </div>
                            <div class="col-sm-2">
                                <input class="form-control" v-model="static" placeholder="Static +X">
                            </div>
                            <div class="col-sm-2">
                                <button class="btn btn-primary" v-on:click="roll">Roll</button>
                            </div>
                        </div>
                    </div>
                    <hr>
                    <div id="history">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>When</th>
                                    <th>Who</th>
                                    <th>Dice</th>
                                    <th>Result</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="entry in history" transition="">
                                    <td>{{ entry.date }}</td>
                                    <td>{{ entry.name }}</td>
                                    <td>{{ entry.dice }}</td>
                                    <td>{{ entry.result }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <div class="clearfix">
                        <h3 class="pull-left panel-title">People</h3>
                        <a v-on:click="leave" id="btn_leave"><span class="pull-right label label-danger">Leave</span></a>
                    </div>
                </div>
                <div class="panel-body">
                    <div>
                        <p id="users">
                            <span v-for="name in activeUsers">
                                {{ name }}<br>
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">How to use this app</h3>
                </div>
                <div class="panel-body">
                    <p>
                        In the three textboxes at the top of the screen in the middle, input the number of dice
                        you have for the test's relevant <strong>ability</strong> in the first box, the number
                        of any <strong>bonus</strong> dice you get to add to the test in the second, and any
                        static modifier in the third.
                        Then, click <strong>Roll</strong>.
                        <br><br>
                        Your rolls and everyone else's rolls will appear in the middle of the screen in reverse
                        chronological order (so the most recent rolls are at the top). The "Result" column shows your 
                        results in the order <code>raw rolls -> top dice you keep -> final value</code>.
                        <br><br>
                        If you need to change your name, use the <strong>Leave</strong> link in the upper-right of the
                        screen to go back to the sign-in page.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import store from './store'

export default {
    data () {
        return {
            history: [],
            activeUsers: [],
            ability : 2,
            bonus : 0,
            static : 0,
            connected: false,
            hasConnected: false,
            store
        }
    },
    ready() {
        this.getHistory()
        let store = this.store
        this.$socket.emit('setname', {name: this.store.state.name}, function() {
            console.log('socket: setname = ' + store.state.name + ' ->')
        })
    },
    sockets: {
        connect: function() {
            console.log('<- sockets: Connected to the backend web socket server')
            this.connected = true
            this.hasConnected = true
        },
        disconnect: function() {
            console.log('<- sockets: Disconnected from the backend web socket server')
            this.connected = false
        },
        roll_event: function() {
            console.log('<- sockets: roll_event')
            this.getHistory()
        },
        users: function(data) {
            console.log('<- sockets: users')
            this.activeUsers = data.users
        }
    },
    methods: {
        getHistory: function() {
            console.log('http: history ->')
            this.$http.get('http://localhost:13493/history').then((response) => {
                this.$set('history', response.data.history)
            })
        },
        roll: function() {
            console.log('sockets: roll ->')
            this.$socket.emit('roll_request', {
                ability: this.ability,
                bonus: this.bonus,
                static: this.static
            })
        },
        leave: function() {
            console.log('sockets: leave ->')
            let router = this.$router
            this.$socket.emit('leave', function() {
                router.go('/')
            })
        }
    }
}
</script>

<style>
body {
    padding-top: 1em;
    background-color: rgba(0, 0, 0, 0.02);
    font-family: 'Roboto', sans-serif;
    font-size: 1.5em;
}

div.container-large {
    width: 90%;
    margin-left: auto;
    margin-right: auto;
}

span.loading {
    color: gray;
}

h3.nomartop {
    margin-top: 0;
}

a#btn_leave {
    cursor: pointer;
}

p#error {
    background-color: rgba(255, 0, 0, 0.5);
    padding: 5px;
    color: black;
    font-size: 1.5em;
}
.fade-transition {
    transition: opacity .5s ease;
}
.fade-enter, .fade-leave {
    opacity: 0;
}
div.container > h2 {
    margin-top: 0;
}
</style>
