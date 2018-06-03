<template>
  <div class ="inference">
    <b-row class = "pt-3 ml-5">
      <h-6 style ="font-size: 1.7rem">Run inference</h-6>
    </b-row>
    <double-map></double-map>
  </div>
</template>

<script>
import DoubleMap from './DoubleMap'
import MapSeries from './MapSeries'
export default {
  name: 'Inference',
  components: {MapSeries, DoubleMap},
  data () {
    return {
      msg: 'Run inference'
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
