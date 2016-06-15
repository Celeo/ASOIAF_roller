<template>
<div id="app">

</div>
</template>

<script>
import Vue from 'vue'
import VueSocketio from 'vue-socket.io'


Vue.use(VueSocketio, 'http://localhost:5000')

export default {
    data () {
        return {
            //
        }
    },
    computed: {
        //
    },
    sockets: {
        connect: function() {
            console.log('Connected to the backend web socket server')
        },
        disconnect: function() {
            console.log('Disconnected from the backend web socket server')
        },
        event: function(data) {
            console.log('Got event: ' + data.message)

        },
        response: function(data) {
            console.log('Got response: ' + data.message)

        }
    },
    methods: {
        // 
    }
}
</script>

<style>

</style>
