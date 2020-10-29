<template>
  <div class="GraphTypeSchoolAttendance">
    <h2>Närvaro och frånvaro</h2>
    <div class="columns">
      <div>
        <h3>Total närvaro och frånvaro:</h3>
        <canvas :id="'myChart' + _uid" width="600" height="400" />
      </div>

      <div>
        <h3>Frånvaro i dietgrupper</h3>

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

      <!--div>
        <h5>Viktiga frånvarande:</h5>

        <ul>
          <li v-for="p in highlighted" :key="p">
            {{ p }}
          </li>
        </ul>
      </div-->
    </div>

    <!--hr-->

    <!--div class="columns">
      <div>
        Samtliga frånvarande:
        <ul>
          <li v-for="(p, i) in this.absence" :key="i">
            {{ p.givenName }} {{ p.familyName }}
          </li>
        </ul>
      </div>
      <div>
        Lista som Viktig frånvarande:
        <ul>
          <li
            v-for="(p, i) in this.highlightList"
            :key="i"
            class="remove"
            @click="removeHighlight(i)"
          >
            {{ p }}
          </li>
        </ul>
        <form @submit.prevent="addHighlight">
          <input name="person" type="text">
          <button type="submit">
            Lägg till
          </button>
        </form>
        <p class="small">
          Klicka på ett namn för att ta bort från listan
        </p>
      </div>
    </div-->
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
    dietGroups: function () {
      return this.graph.endpointData.values[2];
    }
    /* highlighted: function () {
      return this.absence.absentList.filter(value =>
        this.highlightList.includes(value)
      );
    } */
  },
  mounted: function () {
    this.initGraph();
  },
  methods: {
    initGraph: function () {
      const ctx = document
        .getElementById('myChart' + this._uid)
        .getContext('2d');
      this.myChart = new Chart(ctx, this.chartSettings(this.absence));
    },
    chartSettings: function (entity) {
      return {
        type: 'bar',
        data: {
          labels: ['Närvarande', 'Frånvarande'],
          datasets: [
            {
              data: [this.school.studentCount, this.absence.length],
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
