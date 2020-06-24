<template>
  <div class="Chart">
    <h4>{{ chart.data.name }}</h4>
    <canvas :id="'myChart' + _uid" width="600" height="400" />
  </div>
</template>

<script>

import Chart from 'chart.js'; // NOTE! npm package Chart.js
import chartTypes from '../js/models/chart-types'; // path needs to be fixed

export default {
  name: 'Chart',
  components: {
    // ComponentName
  },
  props: {
    chart: { type: Object, default: function () { return {}; } } // Feels like overkill, but eslint wants default type that needs to be a function!?
  },
  data: function () {
    return {
      myChart: undefined
    };
  },
  computed: {
  },
  mounted: function () {
    this.initChart();
  },
  methods: {
    initChart: function () {
      const ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      this.myChart = new Chart(ctx, chartTypes[this.chart.data.type](this.chart.data.values));
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Chart {
}

canvas {
  max-width: 400px;
  max-height: 400px;
}
</style>
