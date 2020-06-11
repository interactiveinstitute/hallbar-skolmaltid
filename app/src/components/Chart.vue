<template>
  <div class="Chart">
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
    data: Object
  },
  data: function () {
    return {
      myChart: undefined,
      ctx: undefined
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
    this.initChart();
  },
  methods: {
    initChart: function () {
      this.ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      if (this.data.type === 'presence') {
        this.chartPresence(this.data.data);
      } else if (this.data.type === 'waste') {
        this.chartWaste(this.data.data);
      }
    },
    chartPresence: function (data) {
      this.myChart = new Chart(this.ctx, {
        type: 'bar',
        data: {
          labels: ['Närvarande', 'Frånvarande'],
          datasets: [
            {
              data: [data.present, data.absent],
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
    },
    chartWaste: function (data) {
      this.myChart = new Chart(this.ctx, {
        type: 'pie',
        data: {
          labels: ['Kök', 'Matsal'],
          datasets: [
            {
              data: [data.kitchen, data.canteen],
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
