<template>
  <div class="marker-map p-5">
    <b-row class = "mx-auto">
    <div class="map-container pl-5">
      <v-map
        :zoom.sync="config.zoom" :center.sync="config.center" :min-zoom.sync="config.minZoom" :max-zoom.sync="config.maxZoom"
        @l-click="onMapClick" @l-zoomanim="onZoomChange">
        <v-tilelayer :url="config.url" :attribution="config.attribution" :layerType="base" ></v-tilelayer>
        <l-wms-tile-layer :transparent = "layerPre.transparent" :baseUrl="layerPre.baseUrl" :format = "layerPre.format"
                          :layers="layerPre.layers"  :layerType="layerPre.layerType"/>
      </v-map>
    </div>
    <div class="map-container pl-5">
      <v-map
        :zoom.sync="config.zoom" :center.sync="config.center" :min-zoom.sync="config.minZoom" :max-zoom.sync="config.maxZoom"
        @l-click="onMapClick" @l-zoomanim="onZoomChange">
        <v-tilelayer :url="config.url" :attribution="config.attribution" :layerType="base" ></v-tilelayer>
        <l-wms-tile-layer :transparent = "layerPost.transparent" :baseUrl="layerPost.baseUrl" :format = "layerPost.format"
                          :layers="layerPost.layers"  :layerType="layerPost.layerType"/>
      </v-map>
    </div>
    </b-row>
  </div>
</template>

<script>
import Vue2Leaflet from 'vue2-leaflet'
import MapModel from './map-model'
import WMSLayer from './wms-layer'

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
      default: new MapModel([34.30, -119.20])
    },
    layerPost:
      {
        type: Object,
        default: new WMSLayer('opm-host:ventura_channel_PBLU')
      },
    layerPre:
      {
        type: Object,
        default: new WMSLayer('opm-host:ventura_channel_BLU')
      },
    'zoom-changed': {
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
    'v-tilelayer': Vue2Leaflet.LTileLayer,
    'l-wms-tile-layer': Vue2Leaflet.LWMSTileLayer
  },
  methods: {
    onZoomChange (event) {
      this.$emit('zoom-changed', event.target.getZoom())
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
      width: 40%;
      height: 540px;
    }
  }
</style>
