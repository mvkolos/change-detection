<template>
  <div>
    <b-container class="pt-5">
      <b-row>
        <b-col col md="4" v-for="dataset in datasets" :key="dataset.name">
          <b-card :title="dataset.displayName"
                  :img-src = "dataset.imageUrl"
                  img-alt="Img"
                  img-top>
            <p class="card-text">{{dataset.description}}</p>
            <b-button href="/inference" variant="primary">View Changes</b-button>
          </b-card>
        </b-col>
        <b-col col md="4">
          <b-card title="Your data">
            <div>
              <!-- Styled -->
              <b-form-file class = "p-3" v-model="filePre" ref="filePre" :state="Boolean(filePre)" placeholder="Choose an image 'pre'" @change="onFileChange"></b-form-file>
              <b-form-file class = "p-3" v-model="filePost" ref="filePost" :state="Boolean(filePost)" placeholder="Choose an image 'post'"></b-form-file>
              <b-form-file class = "p-3" v-model="fileMarkup" ref="fileMarkup" :state="Boolean(fileMarkup)" placeholder="Upload markup (optional)"></b-form-file>
              <b-button @click = postDataset() class = "mt-4" variant="primary">Submit</b-button>

              <!--&lt;!&ndash; Plain mode &ndash;&gt;-->
              <!--<b-form-file v-model="file2" class="mt-3" plain></b-form-file>-->
              <!--<div class="mt-3">Selected file: {{file2 && file2.name}}</div>-->
            </div>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      datasets: [],
      filePre: null,
      filePost: null,
      fileMarkup: null
    }
  },
  mounted () {
    this.fetchDatastes()
  },
  methods:
    {
      fetchDatastes () {
        axios.get('http://localhost:5000/datasets').then(response => {
          this.datasets = response.data.datasets
          console.log('response', response.data)
        })
      },
      postDataset () {
        var data = new FormData()
        data.append('filePre', this.filePre)
        data.append('filePost', this.filePost)
        axios.post('http://localhost:5000/datasets', data)
      },
      onFileChange: function (e) {
        console.log(this.filePre)
      }
    }
}
</script>
