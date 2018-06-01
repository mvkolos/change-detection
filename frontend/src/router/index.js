import Vue from 'vue'
import Router from 'vue-router'
import Inference from '@/components/Inference'
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Inference',
      component: Inference
    }
  ]
})
