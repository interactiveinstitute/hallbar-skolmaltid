<template>
  <div class="GraphTypeAttendanceLongterm">
    <h2>
      Elevnärvaro, långsiktig planering
    </h2>
    <div class="info">
      <p>
        Graferna visar beräknad närvaro och anmäld frånvaro för {{ graph.endpointData.values[0].name }} ({{ graph.endpointData.values[0].studentCount }} elever) mellan angivna
        datum.
      </p>
      <label> Startdatum: <input v-model="dateStart" type="date"> </label>
      <label> Slutdatum: <input v-model="dateEnd" type="date"> </label>
    </div>

    <div class="columns border">
      <div class="padding">
        <h3>Samtliga elever</h3>
        <canvas :id="'chartAll' + _uid" />
      </div>
      <div class="padding">
        <h3>Elever med specialkost</h3>
        <canvas :id="'chartPresence' + _uid" />
      </div>
    </div>
  </div>
</template>

<script>
import utils from '../../js/utils';
import backendUtils from '../../js/backend-utils';
import Chart from 'chart.js'; // NOTE! npm package Chart.js

export default {
  name: 'GraphTypeAbsenceStacked',
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
      chartAll: undefined,
      myChart: undefined,
      dateSelected: '2020-11-05',
      dateStart: '',
      dateEnd: ''
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
      return this.graph.endpointData.values[1][0].absent;
    },
    absenceNoDiet: function () {
      return this.absence.filter(a => !this.hasDiet(a.socialNumber));
    },
    absenceDates: function () {
      const students = {};
      this.absence.forEach((s, i) => {
        students[s.socialNumber] = utils.weekdays(
          utils.getDatesArray(
            s.dateStart,
            s.dateEnd,
            this.dateStart,
            this.dateEnd
          )
        );
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
    chartDates: function () {
      return utils.weekdays(utils.getDatesArray(this.dateStart, this.dateEnd));
    },
    chartDatasetAll () {
      const dataPresence = [];
      const dataAbsence = [];
      this.chartDates.forEach((date, iDate) => {
        const present =
          this.school.studentCount -
          this.absence.filter(a =>
            this.absenceDates[a.socialNumber].includes(date)
          ).length;
        dataPresence.push(present);
        const absent = this.absence.filter(a =>
          this.absenceDates[a.socialNumber].includes(date)
        ).length;
        dataAbsence.push(absent);
      });
      const datasetPresence = this.generateDataset(
        dataPresence,
        'Närvarande',
        'rgb(0,200,0)'
      );
      const datasetAbsence = this.generateDataset(
        dataAbsence,
        'Frånvarande',
        'rgb(200,0,0)'
      );

      return { presence: datasetPresence, absence: datasetAbsence };
    },
    chartDatasetNoDiet () {
      const dataPresence = [];
      const dataAbsence = [];
      this.chartDates.forEach((date, iDate) => {
        const present =
          this.school.studentCount -
          this.absenceNoDiet.filter(a =>
            this.absenceDates[a.socialNumber].includes(date)
          ).length;
        dataPresence.push(present);
        const absent = this.absenceNoDiet.filter(a =>
          this.absenceDates[a.socialNumber].includes(date)
        ).length;
        dataAbsence.push(absent);
      });
      const datasetPresence = this.generateDataset(
        dataPresence,
        'Utan specialkost',
        'rgb(0,200,0)'
      );
      const datasetAbsence = this.generateDataset(
        dataAbsence,
        'Utan specialkost',
        'rgb(200,0,0)'
      );

      return { presence: datasetPresence, absence: datasetAbsence };
    },
    chartDatasetsDietGroups: function () {
      const datasets = [];
      this.dietGroups.forEach((group, iGroup) => {
        const dataPresence = [];
        const dataAbsence = [];

        this.chartDates.forEach((date, iDate) => {
          const present =
            group.socialNumbers.length -
            group.socialNumbers.filter(
              sn =>
                Object.prototype.hasOwnProperty.call(this.absenceDates, sn) &&
                this.absenceDates[sn].indexOf(date) !== -1
            ).length;
          dataPresence.push(present);

          const absent = group.socialNumbers.filter(
            sn =>
              Object.prototype.hasOwnProperty.call(this.absenceDates, sn) &&
              this.absenceDates[sn].indexOf(date) !== -1
          ).length;
          dataAbsence.push(-absent);
        });

        const datasetPresence = this.generateDataset(
          dataPresence,
          group.name,
          'rgb(0,' + ((iGroup + 1) * 255) / this.dietGroups.length + ',0)'
        );
        const datasetAbsence = this.generateDataset(
          dataAbsence,
          group.name,
          'rgb(' + ((iGroup + 1) * 255) / this.dietGroups.length + ',0,0)'
        );

        // datasetPresence.stack = 'stackPresence';
        // datasetAbsence.stack = 'stackAbsence';

        datasets.push({ presence: datasetPresence, absence: datasetAbsence });
      });

      return datasets;
    },
    chartDatasets: function () {
      return this.chartDatasetsDietGroups;
    }
  },
  watch: {
    dateStart: function () {
      this.initGraphs();
    },
    dateEnd: function () {
      this.initGraphs();
    }
  },
  mounted: function () {
    const date = new Date();
    this.dateStart = date.toLocaleDateString();
    date.setDate(date.getDate() + 13);
    this.dateEnd = date.toLocaleDateString();
    // this.dates.end.setDate(this.dates.start.getDate() + 7);
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
      // Chart all
      if (this.chartAll) {
        this.chartAll.destroy();
      }
      const ctxAll = document
        .getElementById('chartAll' + this._uid)
        .getContext('2d');
      this.chartAll = new Chart(ctxAll, this.chartSettingsAll());

      // Chart diet
      if (this.myChart) {
        this.myChart.destroy();
      }
      const ctxPresence = document
        .getElementById('chartPresence' + this._uid)
        .getContext('2d');
      this.myChart = new Chart(ctxPresence, this.chartSettings());
    },
    chartSettingsAll: function () {
      return {
        type: 'line',
        data: {
          labels: this.chartDates,
          datasets: [
            this.chartDatasetAll.presence,
            this.chartDatasetAll.absence
          ]
        },
        options: {
          legend: {
            display: true
          },
          scales: {
            y: {
              // beginAtZero: true
            }
          },
          tooltips: {
            mode: 'index',
            intersect: false
          }
        }
      };
    },
    chartSettings: function () {
      return {
        type: 'bar',
        data: {
          labels: this.chartDates,
          datasets: this.chartDatasets
            .map(g => g.presence)
            .concat(this.chartDatasets.map(g => g.absence))
        },
        options: {
          legend: {
            display: true
          },
          scales: {
            xAxes: [{ stacked: true }],
            yAxes: [{ stacked: true }],
            y: {
              beginAtZero: true
            }
          },
          tooltips: {
            mode: 'index',
            intersect: false
          }
        }
      };
    },
    generateDataset: function (data, label, color) {
      return {
        data: data,
        label: label,
        backgroundColor: color,
        borderColor: color,
        borderWidth: 3,
        fill: false,
        lineTension: 0
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
    hasDiet: function (socialNumber) {
      let val = false;
      this.dietGroups.forEach((d, iDiet) => {
        if (d.socialNumbers.includes(socialNumber)) {
          val = true;
        }
      });
      return val;
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
}
.remove {
  cursor: no-drop;
}
.small {
  font-size: small;
  color: gray;
}
</style>
