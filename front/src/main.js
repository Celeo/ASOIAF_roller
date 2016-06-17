import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import App from './App.vue'
import Login from './Login.vue'
import store from './store'


Vue.use(VueResource)
Vue.http.options.root = '/'
Vue.http.options.emulateJSON = true

Vue.use(VueRouter)
let router = new VueRouter({
    hashbang: false,
    history:  true
})
router.redirect({
    '/': '/login',
    '*': '/login'
})
router.map({
    '/login': {
        component: Login,
        name: 'login'
    },
    '/app': {
        component: App,
        name: 'app'
    }
})
router.beforeEach(function(transition) {
    if (transition.to.path === '/app') {
        if (store.state.name === '') {
            transition.abort()
            return
        }
    }
    transition.next()
})

let Root = Vue.extend({})

router.start(Root, '#app')
