<template>
  <div class="RestTest">
    <q-btn color="primary" label="Hämta skolmåltidsdata" @click="loadData" class="q-ma-md"></q-btn>
    <div v-if="result">
      <p>
        Skolmåltids-API:t är under utveckling.
      </p>
      <p>
         Här är istället dagens rymdbild hämtad via NASAs API: <a :href="result.url" target="_blank">{{result.title}}</a>
      </p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'RestTest',
  components: {
  },
  data: function () {
    return {
      result: null
    }
  },
  props: {
  },
  computed: {
  },
  methods: {
    loadData () {
      this.$axios.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
        .then((response) => {
          this.result = response.data
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Loading failed',
            icon: 'report_problem'
          })
        })
    }
  },
  mounted: function () {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.RestTest{
}

</style>
