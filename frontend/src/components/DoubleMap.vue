<template>
  <div class="double-map">
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
        <div>
          <div>
            <b-row>
            <b-button-toolbar class = "px-5" aria-label="Toolbar with button groups and dropdown menu">
              <b-button-group class="px-3">
                <b-btn variant="primary">Run</b-btn>
              </b-button-group>
              <b-dropdown class="mx-1" right text="Method">
                <b-dropdown-item>Segmentation</b-dropdown-item>
                <b-dropdown-item>Classification</b-dropdown-item>
              </b-dropdown>
            </b-button-toolbar>
            </b-row>
            <b-row></b-row>
            <b-row class ="pt-5 pl-5">
              <template>
                <b-table striped hover :items="items"></b-table>
              </template>
           </b-row>
          </div>
        </div>
      </b-row>
    </div>
  </div>
</template>

<script>
import Vue2Leaflet from 'vue2-leaflet'
import MapModel from '../models/map-model'
import WMSLayer from '../models/wms-layer'
const items = [
  { f1: 0.94, IoU: 0.80, method: 'Segmentation' },
  { f1: 0.97, IoU: 0.96, method: 'Classification' }
]
export default {
  name: 'double-map',
  data () {
    return {
      items: items
    }
  },
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
        default: new WMSLayer('opm-host:masked')
      },
    layerPre:
      {
        type: Object,
        default: new WMSLayer('opm-host:rgb_v_pre')
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
