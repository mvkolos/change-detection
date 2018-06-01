<template>
  <div id="app">
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand href="#">Aerial Imagery Change Detection using Deep Learning Methods</b-navbar-brand>
    </b-navbar>
    <b-tabs class = "p-5">
      <b-tab title="Data" active>
        <br>Select data
      </b-tab>
      <b-tab title="Inference" >
        <br>Run inference
      </b-tab>
      <b-tab title="Export" disabled>
        <br>Export masks
      </b-tab>
    </b-tabs>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
  @import './styles/custom-bootstrap.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
</style>
