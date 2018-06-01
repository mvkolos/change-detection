<template>
  <div class="marker-map">
    <div class="map-container px-5">
      <v-map
        :zoom="config.zoom" :center="config.center" :min-zoom="config.minZoom" :max-zoom="config.maxZoom"
        @l-click="onMapClick" @l-zoomanim="onZoomChange">
        <v-tilelayer :url="config.url" :attribution="config.attribution"></v-tilelayer>
      </v-map>
    </div>
  </div>
</template>

<script>
import Vue2Leaflet from 'vue2-leaflet'
import MapModel from './map-model'
// See open issue: https://github.com/Leaflet/Leaflet/issues/4968

export default {
  name: 'marker-map',
  props: {
    'is-shown': {
      type: Boolean,
      default: false
    },
    config: {
      type: Object,
      default: new MapModel()
    },
    'zoom-changed': {
      type: Function,
      default: () => {}
    },
    'marker-moved': {
      type: Function,
      default: () => {}
    },
    'marker-drag-end': {
      type: Function,
      default: () => {}
    },
    'map-clicked': {
      type: Function,
      default: () => {}
    }
  },
  components: {
    'v-map': Vue2Leaflet.LMap,
    'v-tilelayer': Vue2Leaflet.LTileLayer
  },
  methods: {
    onZoomChange (event) {
      this.$emit('zoom-changed', event.target.getZoom())
    },
    onMarkerMove (event) {
      this.$emit('marker-move', event)
    },
    onMarkerDragEnd (event) {
      this.$emit('marker-drag-end', event)
    },
    onMapClick (event) {
      this.$emit('map-click', event)
    }
  }
}
</script>

<style lang="scss">
  .marker-map {
    .map-container {
      width: 50%;
      height: 400px;
    }
  }
</style>
