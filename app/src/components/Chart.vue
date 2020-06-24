<template>
  <div class="Chart">
    <h4>{{ name }}</h4>
    <canvas :id="'myChart' + _uid" width="600" height="400" />
  </div>
</template>

<script>
// import { mapState, mapGetters } from 'vuex'
// import ComponentName from '@/components/ComponentName.vue'

import Chart from 'chart.js';

export default {
  name: 'Chart',
  components: {
    // ComponentName
  },
  props: {
    chart: Object
  },
  data: function () {
    return {
      myChart: undefined,
      ctx: undefined,
      name: ''
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
    this.initChart();
  },
  methods: {
    initChart: function () {
      this.ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      if (this.chart.data.type === 'attendance') {
        this.name = 'Närvaro och frånvaro';
        this.chartAttendance(this.chart.data.values);
      } else if (this.chart.data.type === 'waste') {
        this.chartWaste(this.chart.data.values);
      }
    },
    chartAttendance: function (values) {
      this.myChart = new Chart(this.ctx, {
        type: 'bar',
        data: {
          labels: ['Närvarande', 'Frånvarande'],
          datasets: [
            {
              data: [values[0].attendance.value.present.value, values[0].attendance.value.absent.value],
              backgroundColor: [
                'rgba(99, 255, 132, 0.2)',
                'rgba(255, 99, 132, 0.2)'
              ],
              borderWidth: 1
            }
          ]
        },
        options: {
          legend: {
            display: false
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
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
