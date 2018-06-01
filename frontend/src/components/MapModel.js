import L from 'leaflet'

class MapModel {
  constructor () {
    this.zoom = 2
    this.center = L.latLng(51.505, -0.09)
    this.url = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
    this.attribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    this.minZoom = 1
    this.maxZoom = 20
    this.opacity = 0.6
  }
}

export default MapModel