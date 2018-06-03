<template>
  <div id="app">
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand href="#">Aerial Imagery Change Detection using Deep Learning Methods</b-navbar-brand>
    </b-navbar>
    <b-nav tabs class ="pl-5 pt-5">
      <b-nav-item :to="{ path: '/data'}" :active.sync="toggle">Data</b-nav-item>
      <b-nav-item :to="{ path: '/inference'}" :active.sync="toggle">Inference</b-nav-item>
      <b-nav-item disabled>Export</b-nav-item>
    </b-nav>
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
    }},
  data () {
    return {
      toggle: false
    }
  }
}
</script>

<style lang="scss">
  @import './styles/custom-bootstrap.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
</style>
