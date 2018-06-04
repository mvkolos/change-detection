<template>
  <div>
    <b-list-group>
        <b-list-group-item v-for="element in series" :key="element.seriesId"
                          button:true b-link :to ="{ path: '/inference', query: { layersPre: element.layerPre, layersPost: element.layerPost }}">{{element.layerPre}}</b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
import {seriesModule} from '../constants'
import {series} from '../store/modules/series'
import store from '../store'
if (!store.state.series) {
  store.registerModule(seriesModule, series)
}
// const items = [
//   { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
//   { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
//   { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
//   { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
// ]
const {
  mapState: mapSeriesState } = createNamespacedHelpers(seriesModule)
export default {
  name: 'Series',
  computed: {
    ...mapSeriesState([seriesModule])
  },
  created: () => { store.dispatch('series/fetchSeries') }
}
</script>
