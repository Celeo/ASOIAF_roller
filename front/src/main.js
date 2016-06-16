import Vue from 'vue'
import App from './App.vue'
import Login from './Login.vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'


Vue.use(VueResource)
Vue.http.options.root = '/'
Vue.http.options.emulateJSON = true

Vue.use(VueRouter)
let router = new VueRouter({
    hashbang: false,
    history:  true
})
router.map({
    '/': {
        component: Login
    },
    '/app': {
        component: App
    }
})

let Root = Vue.extend({})

router.start(Root, '#app')
