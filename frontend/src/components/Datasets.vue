<template>
  <div>
    <b-container>
      <b-row>
        <b-col class = 'p-5'>
          <b-card title="Ventura"
                  img-src = 'http://localhost:5000/image'
                  img-alt="Img"
                  img-top>
            <p class="card-text">
              California wildfires "before/after" imagery
              published by DigitalGlobe.
            </p>
            <b-button href="/inference" variant="primary">View Changes</b-button>
          </b-card>
        </b-col>
        <b-col class = 'p-5'>
          <b-card title="Moscow North"
                  img-src='https://picsum.photos/600/300/?image=25'
                  img-alt="Img"
                  img-top>
            <p class="card-text">
              Open WMTS temporal imagery of
              Moscow Northern districts.
            </p>
            <b-button href="/inference" variant="primary">View Changes</b-button>
          </b-card>
        </b-col>
        <b-col cols="6" md="4" class = 'p-5'>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// import venturaPre from '@/assets/ventura-pre.png'
export default {
  data () {
    return {
      ventura: '../assets/ventura-pre.png'
    }
  }
}
</script>
