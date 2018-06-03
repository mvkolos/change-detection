class WMSLayer {
  constructor (layers) {
    this.baseUrl = 'http://localhost:8081/geoserver/opm-host/wms'
    this.layers = layers
    this.transparent = true
    this.format = 'image/png'
    this.layerType = 'overlay'
  }
}
export default WMSLayer
