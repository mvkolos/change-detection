import axios from 'axios'

import {datasetPath, seriesModule} from '../../constants'
import {LOAD_SUCCESS} from '../mutation-types'
// We're using reusable form modules
// to store the data of our forms.

const actions = {
  fetchSeries ({commit, state}) {
    console.log('fetching series')
    var path = [datasetPath, state.datasetId, seriesModule].join('/')
    axios.get(path).then(response => {
      return commit(LOAD_SUCCESS, response.data)
    })
  }
}
const state = () => ({
  datasetId: '',
  series: [
    {
      seriesId: 0,
      coverUrl: '',
      layerPre: '',
      layerPost: ''}]
})
const mutations = {
  [LOAD_SUCCESS] (state, data) {
    console.log('response ', data.series)
    state.series = data.series
  }}

export const series = {
  namespaced: true,
  actions,
  mutations,
  state
}
