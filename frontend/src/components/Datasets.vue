<template>
  <div>
    <b-container>
      <b-row>
        <b-col col md="4" v-for="dataset in datasets" :key="dataset.name">
          <b-card :title="dataset.displayName"
                  img-src = 'https://picsum.photos/600/300/?image=25'
                  img-alt="Img"
                  img-top>
            <p class="card-text">{{dataset.description}}</p>
            <b-button href="/inference" variant="primary">View Changes</b-button>
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
      datasets: []
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
      }
    }
}
</script>
