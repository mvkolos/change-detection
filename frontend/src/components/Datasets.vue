<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="6" md="4" class = 'p-5'>
          <b-card title="Title"
                  img-src = '../static/ventura-pre.png'
                  img-alt="Img"
                  img-top>
            <p class="card-text">
              This is a wider card with supporting text below as a
              natural lead-in to additional content. This content
              is a little bit longer.
            </p>
            <div slot="footer">
              <small class="text-muted">Last updated 3 mins ago</small>
            </div>
          </b-card>
        </b-col>
        <b-col cols="6" md="4" class = 'p-5'>
          <b-card title="Title"
                  img-src="https://picsum.photos/300/300/?image=41"
                  img-alt="Img"
                  img-top>
            <p class="card-text">
              This is a wider card with supporting text below as a
              natural lead-in to additional content. This content
              is a little bit longer.
            </p>
            <div slot="footer">
              <small class="text-muted">Last updated 3 mins ago</small>
            </div>
          </b-card>
        </b-col>
        <b-col cols="6" md="4" class = 'p-5'>
          <b-card title="Title"
                  img-src="https://picsum.photos/300/300/?image=41"
                  img-alt="Img"
                  img-top>
            <p class="card-text">
              This is a wider card with supporting text below as a
              natural lead-in to additional content. This content
              is a little bit longer.
            </p>
            <div slot="footer">
              <small class="text-muted">Last updated 3 mins ago</small>
            </div>
          </b-card>
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
