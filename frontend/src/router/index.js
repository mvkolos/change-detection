import Vue from 'vue'
import Router from 'vue-router'
// import Inference from '@/components/Inference'
import BootstrapVue from 'bootstrap-vue'
import Vue2Leaflet from 'vue2-leaflet'
import VueLogger from 'vuejs-logger'

const options = {
  // optional : defaults to true if not specified
  isEnabled: true,
  // required ['debug', 'info', 'warn', 'error', 'fatal']
  logLevel: 'debug',
  // optional : defaults to false if not specified
  stringifyArguments: false,
  // optional : defaults to false if not specified
  showLogLevel: false,
  // optional : defaults to false if not specified
  showMethodName: false,
  // optional : defaults to '|' if not specified
  separator: '|',
  // optional : defaults to false if not specified
  showConsoleColors: false
}
const VueUploadComponent = require('vue-upload-component')
Vue.component('file-upload', VueUploadComponent)
Vue.use(VueLogger, options)
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
