export class Series {
  constructor ({layerPre = null, layerPost = null, datasetId = null} = {}) {
    this.layerPre = layerPre
    this.layerPost = layerPost
    this.datasetId = datasetId
  }
}
