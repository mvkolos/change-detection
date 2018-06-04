<template>
  <div class ="inference">
    <b-row class = "pt-3 ml-5">
      <h-6 style ="font-size: 1.7rem">Run inference</h-6>
    </b-row>
    <map-series :layers-post=layersPost :layers-pre=layersPre></map-series>
  </div>
</template>

<script>
import MapSeries from './MapSeries'
export default {
  name: 'Inference',
  components: {MapSeries},
  props: {
    layersPre: {
      type: Text,
      default: 'opm-host:rgb_v_pre'
    },
    layersPost: {
      type: Text,
      default: 'opm-host:rgb_v_pre'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
