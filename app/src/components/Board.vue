<template>
  <div class="Board">
    <div>
      <h3>{{ data.name }}</h3>
      <div v-for="(chart, i) in data.charts" :key="i">
        <Chart :data="chart" />
      </div>
    </div>
    <pre>
      {{ data }}
    </pre>
  </div>
</template>

<script>
// import { mapState, mapGetters } from 'vuex'
import Chart from 'components/Chart.vue';

export default {
  name: 'ComponentTemplate',
  components: {
    Chart
  },
  props: {
    data: Object
  },
  data: function () {
    return {
      // name: "My Name"
    };
  },
  computed: {
    /* ...mapState([
      'myState',
    ]), */
    /* ...mapGetters([
      'myGetter'
    ]) */
  },
  mounted: function () {
    console.log(this.data);
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Board {
  display: flex;
}

pre {
  padding: 5px;
  background: lightgray;
}
</style>
