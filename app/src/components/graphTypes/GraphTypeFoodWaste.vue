<template>
  <div v-if="graph.endpointData" class="GraphTypeFoodWaste">
    <div class="info">
      <h2 class="text-white">
        Matsvinn ({{ dateSelected }})
      </h2>
      <p>
        Matsvinn i gram/person för {{ schoolSelected.name }}.
      </p>
    </div>
    <div class="border q-pa-md">
      <div>
        <canvas :id="'chart' + _uid" ref="canvas" />
      </div>
      <div v-if="!wasteSelectedDate" class="text-negative">
        Inget matsvinn är registrerat för {{ dateSelected }}.
      </div>
    </div>

    <!--pre>
      {{ wasteSelectedDate }}
    </pre-->
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import Chart from 'chart.js/auto'; // NOTE! npm package Chart.js
import ChartDataLabels from 'chartjs-plugin-datalabels';
Chart.register(ChartDataLabels);

export default {
  name: 'GraphTypeFoodWaste',
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
      chartTotal: undefined
    };
  },
  computed: {
    ...mapState('user', ['schoolSelectedId', 'dateSelected']),
    ...mapGetters('user', ['schoolSelected']),
    waste () {
      return this.graph.endpointData.values[1];
    },
    wasteSelectedDate () {
      return this.waste.find(m => m.date.substring(0, 10) === this.dateSelected);
    }
  },
  watch: {
    'graph.endpointData' () {
      console.log('Graph endpoint data changed');
      this.updateGraphData();
    },
    schoolSelectedId () {
      this.loadData();
    },
    dateSelected: function () {
      this.updateGraphData();
    }
  },
  mounted: function () {
    this.loadData();
  },
  updated () {
    if (!this.chartTotal) {
      this.initGraphs();
    }
  },
  methods: {
    endpoints: function (endpointDataRequest) {
      // Required method for all graph types
      return [
        endpointDataRequest.school,
        '?type=FoodWaste&q=refSchool==' + endpointDataRequest.school + '&limit=1000'
      ];
    },
    loadData: function () {
      // Required method for all graph types
      this.$store.dispatch('graphs/setGraphData', {
        graph: this.graph,
        endpointDataRequest: {
          school: this.schoolSelectedId
        }
      });
    },
    initGraphs: function () {
      const canvas = this.$refs.canvas;
      canvas.width = canvas.style['max-width'];
      canvas.height = 400;
      const ctxAll = canvas.getContext('2d');
      this.chartTotal = new Chart(ctxAll, this.chartSettings());
      this.updateGraphData();
    },
    chartSettings: function () {
      return {
        type: 'bar',
        data: {
          labels: ['Kökssvinn', 'Serveringssvinn', 'Tallrikssvinn', 'Totalt svinn']
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            legend: {
              display: false
            },
            datalabels: {
              color: 'white',
              labels: {
                title: {
                  font: {
                    weight: 'bold',
                    size: '20pt'
                  }
                }
              },
              formatter: function (value, context) {
                return value + ' g';
              }
            }
          }
        }
      };
    },
    updateGraphData: function () {
      if (!this.chartTotal) {
        return;
      }
      this.chartTotal.data.datasets = [
        {
          data: this.wasteSelectedDate ? [
            Math.round(this.wasteSelectedDate.kitchenWaste * 1000 * 100) / 100,
            Math.round(this.wasteSelectedDate.plateWaste * 1000 * 100) / 100,
            Math.round(this.wasteSelectedDate.servingWaste * 1000 * 100) / 100,
            Math.round((parseFloat(this.wasteSelectedDate.kitchenWaste) + parseFloat(this.wasteSelectedDate.plateWaste) + parseFloat(this.wasteSelectedDate.servingWaste)) * 1000 * 100) / 100
          ] : [0, 0, 0, 0],
          backgroundColor: ['rgb(250, 130, 0)', 'rgb(230, 150, 0)', 'rgb(210, 170, 0)', 'rgb(200, 0, 0)'],
          borderWidth: 0
        }
      ];
      this.chartTotal.update();
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
canvas {
  max-width: 100%;
  max-height: 400px;
}
</style>
