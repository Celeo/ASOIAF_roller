<template>
<div class="row">
  <div class="col-lg-6 col-md-offset-3">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h1 class="panel-title">Select name</h1>
      </div>
      <div class="panel-body">
        <form v-on:submit.prevent="setName" method="POST">
        <div class="form-group">
          <input type="text" v-model="name" class="form-control" placeholder="Your name" required autofocus>
        </div>
        <button type="submit" class="btn btn-primary">Go</button>
        </form>
      </div>
    </div>
  </div>
</div>
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
