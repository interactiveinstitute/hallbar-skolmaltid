<template>
  <div class="Chart">
    <canvas id="myChart" width="600" height="400" />
    <div>
      <pre>
        {{ data }}
      </pre>
    </div>
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
      this.ctx = document.getElementById('myChart').getContext('2d');
      if (this.data.type === 'presence') {
        this.initPresence(this.data.data);
      }
    },
    initPresence: function (data) {
      this.myChart = new Chart(this.ctx, {
        type: 'bar',
        data: {
          labels: ['Närvarande', 'Frånvarande'],
          datasets: [
            {
              data: [data.present, data.absent],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)'
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
  display: flex;
}

#myChart {
  max-width: 400px;
  max-height: 400px;
}
</style>
