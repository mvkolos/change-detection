<template>
  <div id="app">
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand href="#">Aerial Imagery Change Detection using Deep Learning Methods</b-navbar-brand>
    </b-navbar>
    <b-tabs class ="p-5">
      <b-tab title="Data" active>
        <br>Select data
      </b-tab>
      <b-tab title="Inference" >
        <br>Run inference
      </b-tab>
      <b-tab title="Export" disabled>
        <br>Disabled
      </b-tab>
    </b-tabs>
    <!--<b-nav tabs class = "pl-5 pt-5">-->
      <!--<b-nav-item active = "data_active">Data</b-nav-item>-->
      <!--<b-nav-item >Inference</b-nav-item>-->
      <!--<b-nav-item disabled>Export</b-nav-item>-->
    <!--</b-nav>-->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    redirect (path) {
      window.location.replace(path)
    }}
}
</script>

<style lang="scss">
  @import './styles/custom-bootstrap.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
</style>
