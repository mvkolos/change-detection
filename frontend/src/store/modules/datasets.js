import axios from 'axios'

// Models are used to prepare
// store data to be sent to an API.
// import { createDataset } from '../../models/dataset-model'

// import { GET_DATASETS } from '../action-types'
import { LOAD_SUCCESS } from '../mutation-types'
import {datasetPath} from '../../constants'
// We're using reusable form modules
// to store the data of our forms.

const actions = {
  fetchDatasets ({commit}) {
    console.log('fetching datasets')
    axios.get(datasetPath).then(response => {
      return commit(LOAD_SUCCESS, response.data)
    })
  }
}

const mutations = {
  [LOAD_SUCCESS] (state, data) {
    console.log('response ', data.datasets[0])
    state.datasets = data.datasets
    console.log(state.datasets[0].name)
  }}

const state = () => ({
  datasets: []
})
// // We're exporting datasets field mapper
// // functions for mapping form fields to Vuex.
// // See: https://github.com/maoberlehner/vuex-map-fields#custom-getters-and-mutations
// export const { mapFields: mapAddressFields } = createHelpers({
//   getterType: `customer/address/getField`,
//   mutationType: `customer/address/updateField`
// })
//
// export const { mapMultiRowFields: mapContactMultiRowFields } = createHelpers({
//   getterType: `customer/contact/getField`,
//   mutationType: `customer/contact/updateField`
// })
//
// export const { mapFields: mapNameFields } = createHelpers({
//   getterType: `customer/name/getField`,
//   mutationType: `customer/name/updateField`
// })

export const datasets = {
  namespaced: true,
  actions,
  mutations,
  state
}
