<template>
  <div class="Graph">
    <!--h4>{{ graph.chart.name }}</h4>
    <div v-for="sd in graph.chart.staticData(graph.chart.values)" :key="sd">
      {{ sd }}
    </div>
    <canvas :id="'myChart' + _uid" width="600" height="400" /-->
  </div>
</template>

<script>
import Chart from 'chart.js'; // NOTE! npm package Chart.js

export default {
  name: 'Graph',
  components: {},
  props: {
    graph: {
      type: Object,
      default: function () {
        return {};
      }
    } // Feels like overkill, but eslint wants default type that needs to be a function!?
  },
  data: function () {
    return {
      myChart: undefined
    };
  },
  computed: {},
  mounted: function () {
    this.initGraph();
  },
  methods: {
    initGraph: function () {
      const ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      this.myChart = new Chart(
        ctx,
        this.graph.chart.chartJSData(this.graph.chart.values)
      );
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Graph {
}

canvas {
  max-width: 400px;
  max-height: 400px;
}
</style>
