<template>
  <div class="GraphTypeAttendanceDay">
    <h2>
      Elevnärvaro, dagsvy
    </h2>

    <div class="info">
      <p>
        Graferna visar beräknad närvaro och anmäld frånvaro för {{ graph.endpointData.values[0].name }} ({{ graph.endpointData.values[0].studentCount }} elever) angivet datum.
      </p>

      <label>Datum: <input v-model="dateSelected" required type="date"> </label>
    </div>
    <div class="columns border">
      <div class="padding">
        <h3>Samtliga elever</h3>

        <div class="flex-center-rows">
          <canvas :id="'chartAll' + _uid" />
          <br>
          <div class="text-h3">
            <strong>{{ school.studentCount - absence.length }}</strong> ({{
              absence.length
            }})
          </div>
        </div>
      </div>

      <div class="padding">
        <h3>Frånvarande elever med specialkost ({{ absenceDiet.length }})</h3>

        <div v-for="(student,i) in absenceDiet" :key="i">
          {{ student.givenName }} {{ student.familyName }} <!--{{ dateRange(student.dateStart, student.dateEnd) }}-->
        </div>

        <!--table>
          <tr>
            <td>
              Kostgrupp
            </td>
            <td>
              Närvarande (frånvarande)
            </td>
            <td>
              Frånvarande
            </td>
          </tr>
          <tr
            v-for="(dg, i) in dietGroups"
            :key="i"
            :class="{
              redrow: dietGroupsAttendance[dg.name].attendance == 0,
              greenrow: dietGroupsAttendance[dg.name].absent.length == 0
            }"
          >
            <td>
              <h4>{{ dg.name }}</h4>
            </td>

            <td>
              <h4>
                <strong>{{ dietGroupsAttendance[dg.name].attendance }}</strong>
                ({{ dietGroupsAttendance[dg.name].absent.length }})
              </h4>
            </td>
            <td>
              <div
                v-for="(p, i) in dietGroupsAttendance[dg.name].absent"
                :key="i"
              >
                {{ p.givenName }} {{ p.familyName }}
                <br>
              </div>
            </td>
          </tr>
        </table-->

        <!--div v-for="(dg, i) in dietGroups" :key="i">
          <h4>{{ dg.name }}</h4>
          <ul>
            <li v-for="(p, i) in absenceByDietGroup(dg)" :key="i">
              {{ p.givenName }} {{ p.familyName }}
            </li>
          </ul>
        </div-->
      </div>
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns';
// import utils from '../../js/utils';
import backendUtils from '../../js/backend-utils';
import Chart from 'chart.js'; // NOTE! npm package Chart.js

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
      dateSelected: ''
    };
  },
  computed: {
    /** @returns {any} */
    highlightList: function () {
      return this.graph.connectedData[0];
    },
    /** @returns {any} */
    school: function () {
      return this.graph.endpointData.values[0];
    },
    /** @returns {any} */
    absence: function () {
      const absences = this.graph.endpointData.values[1];
      // console.log('endpoints 1 data:', data);
      // TODO: Actually compare dates ina reliable manner
      const foundAbsence = absences.find(absenceObj => {
        // const selectedDate = new Date(this.dateSelected).toDateString();
        // console.log('selectedDate :>> ', selectedDate);
        // const testDate = new Date(absenceObj.dateObserved).toDateString();
        // console.log('testDate :>> ', testDate);
        // return testDate === selectedDate;
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
    /* absenceDate: function () {
      const absent = [];
      this.absence.forEach((s, i) => {
        if (
          utils
            .getDatesArray(s.dateStart, s.dateEnd)
            .includes(this.dateSelected)
        ) {
          absent.push(s);
        }
      });
      return absent;
    }, */
    /* dietGroupsAttendance: function () {
      const groups = {};
      this.dietGroups.forEach((dg, i) => {
        const snAttending = dg.socialNumbers.filter(
          sn => !this.absenceDate.map(a => a.socialNumber).includes(sn)
        );
        const snAbsent = dg.socialNumbers.filter(sn =>
          this.absenceDate.map(a => a.socialNumber).includes(sn)
        );
        groups[dg.name] = {
          attendance: snAttending.length,
          absent: snAbsent.map(sn =>
            this.absenceDate.find(a => a.socialNumber === sn)
          )
        };
        // let snAbsent = absenceDate.filter(a => dg.socialNumbers.includes(a));
      });
      return groups;
    } */
    /* highlighted: function () {
      return this.absence.absentList.filter(value =>
        this.highlightList.includes(value)
      );
    } */
  },
  watch: {
    dateSelected: function () {
      // this.initGraphs();
      this.updateGraphData();
    }
  },
  mounted: function () {
    const date = new Date();
    // this.dateSelected = date.toLocaleDateString();
    this.dateSelected = format(date, 'yyyy-MM-dd');

    this.initGraphs();
  },
  methods: {
    endpoints: function (attached) {
      // Required method for all graph types
      return [
        attached[0],
        // '?type=SchoolAbsenceReported&q=refSchool==' + attached[0],
        '?type=SchoolAttendanceObserved&q=refSchool==' + attached[0],
        '?type=DietGroup&q=refSchool==' + attached[0]
      ];
    },
    initGraphs: function () {
      console.log('Init graphs');
      // Chart all
      const ctxAll = document
        .getElementById('chartAll' + this._uid)
        .getContext('2d');
      this.chartTotal = new Chart(ctxAll, this.chartSettingsAll());
    },
    chartSettingsAll: function () {
      return {
        type: 'pie',
        data: {
          labels: ['Närvarande', 'Frånvarande'],
          datasets: [
            {
              /* data: [
                this.school.studentCount - this.absence.length,
                this.absence.length
              ], */
              backgroundColor: ['rgb(0, 200, 0)', 'rgb(200, 0, 0)'],
              borderWidth: 0
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
          },
          tooltips: {
            mode: 'dataset'
          }
        }
      };
    },
    updateGraphData: function () {
      this.chartTotal.data.datasets = [
        {
          data: [
            this.school.studentCount - this.absence.length,
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
