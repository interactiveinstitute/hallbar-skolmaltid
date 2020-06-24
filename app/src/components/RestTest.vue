<template>
  <div class="RestTest">
    <pre>
      {{ user }}
    </pre>
    <pre>
      {{ school }}
    </pre>
    <!--q-btn color="primary" label="Hämta skolmåltidsdata" class="q-ma-md" @click="loadData" /-->
    <!--pre v-if="result">
        {{ result }}
    </pre-->
  </div>
</template>

<script>

import { mapState } from 'vuex';

export default {
  name: 'RestTest',
  components: {
  },
  props: {
  },
  data: function () {
    return {
      result: null
    };
  },
  computed: {
    ...mapState('user', [
      'user',
      'school'
    ])
  },
  mounted: function () {
    this.loadData();
  },
  methods: {
    loadNasaData () {
      this.$axios.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
        .then((response) => {
          this.result = response.data;
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Loading failed',
            icon: 'report_problem'
          });
        });
    },
    loadData () {
      this.$store.dispatch('user/getUserById', { idUser: 'user1' });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.RestTest{
}

</style>
