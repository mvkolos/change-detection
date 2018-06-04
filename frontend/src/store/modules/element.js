import axios from 'axios'
import {datasetPath} from '../../constants'

const state = () => ({
  datasetId: '',
  seriesId: 0,
  coverUrl: '',
  layerPre: '',
  layerPost: ''})

const actions = {
  requestView ({commit, state}) {
    console.log('requesting inference')
    var path = [datasetPath, 'map_view'].join('/')
    axios.get(path, {params: {datasetId: state.datasetId, seriesId: state.seriesId}})
  },
  postElement ({commit, state}) {
    axios.post(datasetPath, state)
  }
}
export const element = {
  namespaced: true,
  actions,
  state
}
