<template>
  <div>
    <b-row class = "pt-3 ml-5">
      <h-6 style ="font-size: 1.7rem">Select data</h-6>
    </b-row>
    <b-container>
      <b-row>
        <b-col class="py-3" col md="4" v-for="dataset in datasets" :key="dataset.name">
          <b-card :title="dataset.displayName"
                  :img-src = "dataset.coverUrl"
                  img-alt="Img"
                  img-top>
            <p class="card-text">{{dataset.description}}</p>
            <b-button b-link :to ="{ path: '/series', query: { datasetId: dataset.name}}" variant="primary">View Changes</b-button>
          </b-card>
        </b-col>
        <b-col class="py-3" col md="4">
          <b-card align="center" title="Your data">
            <div >
              <div :hidden = "hideCustom">
                <b-form-file class = "p-3 form-control-sm text-left" v-model="filePre" ref="filePre" :state="Boolean(filePre)" placeholder="Choose an image 'pre'" @change="onFileChange"></b-form-file>
                <b-form-file class = "p-3 form-control-sm text-left" v-model="filePost" ref="filePost" :state="Boolean(filePost)" placeholder="Choose an image 'post'"></b-form-file>
                <b-form-file class = "p-3 form-control-sm text-left" v-model="fileMarkup" ref="fileMarkup" :state="Boolean(fileMarkup)" placeholder="Upload markup (optional)"></b-form-file>
              </div>
              <b-button @click="handleUpload" class = "mt-4" variant="primary">Upload</b-button>
            </div>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// import axios from 'axios'
// import { GET_DATASETS } from '../store/action-types'
import { createNamespacedHelpers } from 'vuex'
import {datasetsModule, seriesModule} from '../constants'
import {datasets} from '../store/modules/datasets'
import {series} from '../store/modules/series'
import store from '../store'
if (!store.state.datasets) {
  store.registerModule(datasetsModule, datasets)
}
if (!store.state.series) {
  store.registerModule(seriesModule, series)
}
const {
  mapState: mapDatasetsState
} = createNamespacedHelpers(datasetsModule)
export default {
  data () {
    return {
      element: {
        datasetId: 'ventura',
        seriesId: 0,
        layerPre: 'opm-host:rgb_v_pre',
        layerPost: 'opm-host:rgb_v_post'
      }
    }
  },
  props: {
    hideCustom: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    ...mapDatasetsState([datasetsModule])
  },
  created: () => { store.dispatch('datasets/fetchDatasets') },
  methods:
    {
      // fetchDatastes () {
      //   this.$store.fetchDatastes()
      //   axios.get('http://localhost:5000/datasets').then(response => {
      //     this.datasets = response.data.datasets
      //     console.log('response', response.data)
      //   })
      // },
      // postDataset () {
      //   var data = new FormData()
      //   data.append('filePre', this.filePre)
      //   data.append('filePost', this.filePost)
      //   axios.post('http://localhost:5000/datasets', data)
      // },
      handleUpload () {
        if (this.hideCustom) {
          this.toggleUploadForm(false)
        } else {
          this.postDataset()
        }
      },
      toggleUploadForm (value) {
        this.hideCustom = value
      }
    }
}
</script>
