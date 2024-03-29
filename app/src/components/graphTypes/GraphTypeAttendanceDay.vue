<template>
  <div v-if="graph.endpointData" class="GraphTypeAttendanceDay">
    <div class="info">
      <h2 class="text-white">
        Elevnärvaro ({{ dateSelected }})
      </h2>
      <p>
        Grafen visar beräknad närvaro och anmäld frånvaro för {{ schoolSelected.name }} ({{ schoolSelected.studentCount }} elever).
      </p>
    </div>
    <div class="columns border">
      <div class="q-pa-md">
        <h3>Samtliga elever</h3>

        <div class="flex-center-rows">
          <div>
            <canvas :id="'chartAll' + _uid" ref="canvas" />
          </div>
          <!--br>
          <div class="text-h3">
            <strong class="text-positive">{{ schoolSelected.studentCount - absence.length }}</strong>
            <span class="text-negative"> ({{ absence.length }})</span>
          </div-->
        </div>
      </div>

      <div class="q-pa-md">
        <h3>Frånvarande elever med specialkost ({{ absenceDiet.length }})</h3>

        <div class="list scroll" style="height:150px">
          <q-btn color="primary" @click="showAbsenceDiet = true">
            Visa elever
          </q-btn>
        </div>
      </div>
    </div>

    <q-dialog v-model="showAbsenceDiet">
      <q-card>
        <q-card-section>
          <h3>Frånvarande elever med specialkost ({{ absenceDiet.length }})</h3>
          <div v-for="(student,i) in absenceDiet" :key="i">
            {{ student.givenName }} {{ student.familyName }}
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import backendUtils from '../../js/backend-utils';
import Chart from 'chart.js/auto'; // NOTE! npm package Chart.js
import ChartDataLabels from 'chartjs-plugin-datalabels';
Chart.register(ChartDataLabels);

// Chart.register();

export default {
  name: 'GraphTypeSchoolAttendance',
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
      chartTotal: undefined,
      showAbsenceDiet: false
    };
  },
  computed: {
    ...mapState('user', ['schoolSelectedId', 'dateSelected']),
    ...mapGetters('user', ['schoolSelected']),
    /** @returns {any} */
    absence: function () {
      if (!this.graph.endpointData) {
        return null;
      }
      const absences = this.graph.endpointData.values[1];
      // console.log('endpoints 1 data:', data);
      // TODO: Actually compare dates ina reliable manner
      const foundAbsence = absences.find(absenceObj => {
        return absenceObj.dateObserved.includes(this.dateSelected);
      });
      return foundAbsence ? foundAbsence.absent || [] : [];
    },
    /** @returns {any} */
    absenceDiet: function () {
      return this.absence.filter(s => parseInt(s.socialNumber.substr(9, 2)) < 15);
    },
    /** @returns {any} */
    dietGroups: function () {
      return this.graph.endpointData.values[2];
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
    console.log(this._uid);
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
        '?type=SchoolAttendanceObserved&q=refSchool==' + endpointDataRequest.school + '&limit=1000',
        '?type=DietGroup&q=refSchool==' + endpointDataRequest.school
      ];
    },
    loadData: function () {
      // Required method for all graph types
      console.log('Load data', this.schoolSelectedId);
      this.$store.dispatch('graphs/setGraphData', {
        graph: this.graph,
        endpointDataRequest: {
          school: this.schoolSelectedId
        }
      });
    },
    initGraphs: function () {
      console.log('Init graphs', this.schoolSelectedId);
      const ctxAll = this.$refs.canvas.getContext('2d');
      this.chartTotal = new Chart(ctxAll, this.chartSettingsAll());
      this.updateGraphData();
    },
    chartSettingsAll: function () {
      return {
        type: 'pie',
        data: {
          labels: ['Beräknad närvaro', 'Anmäld frånvaro']
        },
        options: {
          // scales: {
          //   y: {
          //     beginAtZero: true
          //   }
          // },
          plugins: {
            legend: {
              display: true
            },
            tooltip: {
              mode: 'dataset'
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
          data: [
            this.schoolSelected.studentCount - this.absence.length,
            this.absence.length
          ],
          backgroundColor: ['rgb(0, 200, 0)', 'rgb(200, 0, 0)'],
          borderWidth: 0
        }
      ];
      this.chartTotal.update();
    },
    addHighlight: function (event) {
      this.$store.commit('addToArray', {
        array: this.graph.connectedData[0],
        value: event.target.elements.person.value
      });
      backendUtils.updateAttribute(
        this.graph.id,
        'connectedData',
        this.graph.connectedData
      );
    },
    removeHighlight: function (index) {
      this.$store.commit('removeFromArray', {
        array: this.graph.connectedData[0],
        index: index
      });
      backendUtils.updateAttribute(
        this.graph.id,
        'connectedData',
        this.graph.connectedData
      );
    },
    absenceByDietGroup: function (dietGroup) {
      return this.absence.filter(a =>
        dietGroup.socialNumbers.includes(a.socialNumber)
      );
    },
    // TODO: fix ranges. Seems localeDateString returns one day off because of times zones
    dateRange: function (start, end) {
      // const dS = new Date(start).toLocaleDateString();
      // const dE = new Date(end).toLocaleDateString();
      // return dS === dE ? dS : dS + ' - ' + dE;
      const startString = start.substring(0, 10);
      const endString = end.substring(0, 10);
      if (startString === endString) {
        return '';
      } else {
        return `(${startString} - ${endString})`;
      }
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

.columns {
  display: flex;
}
.columns > div {
  flex: 1;
}
.remove {
  cursor: no-drop;
}
.small {
  font-size: small;
  color: gray;
}

table {
  width: 100%;
  border-collapse: collapse;
}

tr {
  background: rgb(240, 240, 200);
}

tr:first-child {
  background: dodgerblue;
  color: white;
}

tr.redrow {
  background: rgb(240, 200, 200);
}

tr.greenrow {
  background: rgb(200, 240, 200);
}

td {
  border: 1px solid white;
  text-align: center;
  padding: 5px;
}
</style>
