import Vue from 'vue'
import Router from 'vue-router'
// import Inference from '@/components/Inference'
import BootstrapVue from 'bootstrap-vue'
import Vue2Leaflet from 'vue2-leaflet'

Vue.use(BootstrapVue)
Vue.use(Router)
Vue.use(Vue2Leaflet)
const routerOptions = [
  { path: '/inference', component: 'DoubleMap' },
  { path: '/data', component: 'Datasets' },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
