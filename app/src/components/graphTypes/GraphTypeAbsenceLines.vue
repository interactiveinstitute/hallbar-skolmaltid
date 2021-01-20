<template>
  <div class="GraphTypeAbsenceLines">
    <h2>Närvaro och frånvaro</h2>
    <div class="columns">
      <div>
        <h3>Total närvaro och frånvaro:</h3>
        <canvas :id="'myChart' + _uid" width="600" height="400" />
      </div>
      <div class="columns">
        <div>
          <h3>Frånvaro i dietgrupper:</h3>

          <div v-for="(dg, i) in dietGroups" :key="i">
            <h4>{{ dg.name }}</h4>
            <ul>
              <li v-for="(p, i) in absenceByDietGroup(dg)" :key="i">
                {{ p.givenName }} {{ p.familyName }}
              </li>
            </ul>
          </div>
        </div>

        <div>
          <h3>Samtliga frånvarande:</h3>
          <ul>
            <li v-for="(p, i) in this.absence" :key="i">
              {{ p.givenName }} {{ p.familyName }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
      myChart: undefined
    };
  },
  computed: {
    highlightList: function () {
      return this.graph.connectedData[0];
    },
    school: function () {
      return this.graph.endpointData.values[0];
    },
    absence: function () {
      return this.graph.endpointData.values[1];
    },
    absenceDates: function () {
      const students = {};
      this.absence.forEach((s, i) => {
        students[s.socialNumber] = this.getDates(s.dateStart, s.dateEnd);
      });
      return students;
    },
    dietGroups: function () {
      return this.graph.endpointData.values[2];
    },
    chartLegends: function () {
      const legends = [];
      this.dietGroups.forEach((group, iGroup) => {
        legends.push(group.name);
      });
      return legends;
    },
    chartLabels: function () {
      return this.getDates('2020-10-15', '2020-11-15');
    },
    chartDatasets: function () {
      const datasets = [];
      this.dietGroups.forEach((group, iGroup) => {
        const color =
          'rgba(' +
          Math.floor(Math.random() * 255) +
          ',' +
          Math.floor(Math.random() * 255) +
          ',' +
          Math.floor(Math.random() * 255) +
          ')';
        const dataset = {
          data: [],
          label: group.name,
          backgroundColor: color,
          borderColor: color,
          borderWidth: 3,
          fill: false,
          lineTension: 0
        };
        // const groupData = [];
        this.chartLabels.forEach((date, iDate) => {
          const absent = group.socialNumbers.filter(
            sn =>
              Object.prototype.hasOwnProperty.call(this.absenceDates, sn) &&
              this.absenceDates[sn].indexOf(date) !== -1
          ).length;
          dataset.data.push(absent);
        });
        datasets.push(dataset);
      });
      console.log(datasets);
      return datasets;
    }
  },
  mounted: function () {
    this.initGraph();
  },
  methods: {
    endpoints: function (attached) {
      // Required method for all graph types
      return [
        attached[0],
        '?type=SchoolAbsenceReported&q=refSchool==' + attached[0],
        '?type=DietGroup&q=refSchool==' + attached[0]
      ];
    },
    initGraph: function () {
      const ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      this.myChart = new Chart(ctx, this.chartSettings(this.absence));
    },
    chartSettings: function (entity) {
      return {
        type: 'line',
        data: {
          labels: this.chartLabels,
          datasets: this
            .chartDatasets /* [
            {
              data: [10, 15, 12],
              backgroundColor: 'rgba(99, 255, 132)',
              borderWidth: 2,
              fill: false
            },
            {
              data: [0, 20, 14],
              backgroundColor: 'rgba(99, 0, 132)',
              borderWidth: 2,
              fill: false
            }
          ] */
        },
        options: {
          legend: {
            display: true
            // labels: this.legends
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      };
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
    getDates: function (start, end) {
      var dateArray = [];
      const dateStart = new Date(start);
      const dateEnd = new Date(end);
      const currentDate = new Date(start);
      for (
        let i = 0;
        i < (dateEnd.getTime() - dateStart.getTime()) / (1000 * 3600 * 24);
        i++
      ) {
        dateArray.push(new Date(currentDate).toLocaleDateString());
        currentDate.setDate(currentDate.getDate() + 1);
      }
      return dateArray;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Graph {
}

canvas {
  max-width: 100%;
  max-height: 100%;
}

.columns {
  display: flex;
}
.columns > div {
  flex: 1;
  margin: 1em;
}
.remove {
  cursor: no-drop;
}
.small {
  font-size: small;
  color: gray;
}
</style>
