<template>
  <div class="Board">
    <div>
      <h3>Mitt bräde</h3>
      <div v-for="(chart, i) in charts" :key="i">
        <Chart :chart="chart" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Chart from 'components/Chart.vue';

export default {
  name: 'ComponentTemplate',
  components: {
    Chart
  },
  props: {
  },
  data: function () {
    return {
      // name: "My Name"
    };
  },
  computed: {
    ...mapState('charts', [
      'charts'
    ])
  },
  mounted: function () {
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Board {
  display: flex;
}

.Board > * {
  flex: 1;
}

pre {
  padding: 5px;
  background: rgb(240, 240, 240);
  border-left: 1px solid lightgray;
  margin: 10px;
}
</style>
