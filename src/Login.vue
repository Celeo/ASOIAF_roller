<template lang="pug">
div.row
  div.col-lg-6.col-md-offset-3
    div.panel.panel-default
      div.panel-heading
        h1.panel-title Select name
      div.panel-body
        form(v-on:submit.prevent="setName" method="POST")
        div.form-group
          input.form-control(v-model="name" placeholder="Your name" required autofocus)
        button.btn.btn-primary(type="submit") Go
</template>

<script>
import Vue from 'vue'


export default {
  data() {
    return {
      name: ''
    }
  },
  methods: {
    setName: function() {
      let router = this.$router
      sessionStorage.setItem('name', this.name)
      this.$socket.emit('setname', {name: this.name}, function() {
        router.go('/app')
      })
    }
  }
}
</script>
