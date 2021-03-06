import Vue from 'vue'
import Router from 'vue-router'
import BootstrapVue from 'bootstrap-vue'
import Vue2Leaflet from 'vue2-leaflet'
import VueLogger from 'vuejs-logger'

Vue.use(VueLogger)
Vue.use(BootstrapVue)
Vue.use(Router)
Vue.use(Vue2Leaflet)

const routerOptions = [
  { path: '/inference',
    component: 'Inference',
    props: (route) => ({
      layersPre: route.query.layersPre,
      layersPost: route.query.layersPost
    })
  },
  { path: '/data', component: 'Datasets' },
  { path: '/series', component: 'Series' },
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
