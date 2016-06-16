<template>
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
                            <tr v-for="entry in history">
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
                        <span v-for="name in names">
                            {{ name }}
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
                    In the two textboxes at the top of the screen in the middle, input the number of dice
                    you have for the test's relevant <strong>ability</strong> in the first box, and the number
                    of any <strong>bonus</strong> dice you get to add to the test. Then, click <strong>Roll</strong>.
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
</template>

<script>
import Vue from 'vue'
import VueSocketio from 'vue-socket.io'


Vue.use(VueSocketio, 'http://localhost:5000/socket.io');

export default {
    data () {
        return {
            history: [],
            users: [],
            ability : 2,
            bonus : 0,
            static : 0
        }
    },
    ready() {
        this.getHistory()
    },
    sockets: {
        connect: function() {
            console.log('Connected to the backend web socket server')
        },
        disconnect: function() {
            console.log('Disconnected from the backend web socket server')
        },
        roll_event: function() {
            console.log('roll_event')
            this.getHistory()
        },
        users: function(data) {
            this.users = data.users
        }
    },
    methods: {
        getHistory: function() {
            console.log('Loading history from backend ...')
            this.$http.get('http://localhost:5000/history').then((response) => {
                this.$set('history', response.data.history)
                console.log('History loaded')
            })
        },
        roll: function() {
            console.log('roll')
            this.$socket.emit('roll_request', {
                ability: this.ability,
                bonus: this.bonus,
                static: this.static
            })
        },
        leave: function() {
            console.log('leave')
            this.$http({
                url: 'http://localhost:5000/leave',
                method: 'GET'
            }).then((response) => {
                this.$router.go('/')
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
</style>
