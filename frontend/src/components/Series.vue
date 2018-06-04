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
const {
  mapState: mapSeriesState } = createNamespacedHelpers(seriesModule)
export default {
  name: 'Series',
  props: {
    datasetId: {
      type: Text,
      default: 'ventura'
    }
  },
  computed: {
    ...mapSeriesState([seriesModule])
  },
  created: () => { store.dispatch('series/fetchSeries') }
}
</script>
