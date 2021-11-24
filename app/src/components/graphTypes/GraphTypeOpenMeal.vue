<template>
  <div v-if="graph.endpointData" class="GraphTypeOpenMeal">
    <div class="info">
      <h2 class="text-white">
        Måltidsinnehåll ({{ dateSelected }})
      </h2>
    </div>
    <div class="border q-pa-md">
      <div v-if="mealSelectedDate">
        <div v-for="(course,iCourse) in mealSelectedDate.courses" :key="iCourse">
          <h3> {{ course.name }}</h3>
          <h4>Klimatavtryck <span class="text-grey-8">(kg CO2e/normalpotion)</span></h4>
          <div>
            <q-chip :color="course.co2Equivalents > 0.5 ? 'negative' : 'positive'" text-color="white" dense>
              {{ course.co2Equivalents }} kg CO2e
            </q-chip>
            {{ Math.round(course.co2Equivalents / 0.5 * 100 * 100) / 100 }}% av <a href="https://www.wwf.se/mat-och-jordbruk/one-planet-plate/" target="_blank">
              WWFs klimatbudget per måltid</a> (0.5 kg CO2e).
          </div>
          <div class="flex row">
            <div class="col">
              <h4>Ingredienser</h4>
              <ul>
                <li v-for="(ing,iIng) in course.ingredientsLabel.split(', ')" :key="iIng">
                  {{ ing }}
                </li>
              </ul>
            </div>
            <div class="col">
              <h4>Allergener</h4>
              <ul v-if="course.possibleAllergens.length" class="text-negative">
                <li v-for="(allergen,iAllergen) in course.possibleAllergens" :key="iAllergen" class="text-bold">
                  {{ allergen }}
                </li>
              </ul>
              <span v-else>Inga allergener</span>
            </div>
            <div class="col">
              <h4>Näringsämnen <span class="text-grey-8">(per normalpotion)</span></h4>
              <div v-for="(nut, iNut) in course.nutrients" :key="iNut">
                <strong>{{ nut.name }}: </strong> {{ nut.amount }} {{ nut.unit }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-negative">
        Måltider är ej planerade för {{ dateSelected }}.
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
// import { format } from 'date-fns';
import utils from '../../js/utils';
// import Chart from 'chart.js'; // NOTE! npm package Chart.js

export default {
  name: 'GraphTypeOpenMeal',
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
    };
  },
  computed: {
    ...mapState('user', ['schoolSelectedId', 'dateSelected']),
    ...mapGetters('user', ['schoolSelected']),
    meals () {
      return this.graph.endpointData.values[1];
    },
    dateToday () {
      const date = new Date();
      return date.toLocaleDateString();
    },
    mealSelectedDate () {
      return this.meals.find(m => m.date.substring(0, 10) === this.dateSelected);
    }
  },
  watch: {
    schoolSelectedId () {
      this.loadData();
    }
  },
  mounted: function () {
    this.loadData();
  },
  updated () {
  },
  methods: {
    endpoints: function (endpointDataRequest) {
      // Required method for all graph types
      return [
        endpointDataRequest.school,
        '?type=OpenMeal&q=refSchool==' + endpointDataRequest.school + '&limit=1000'
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
    CO2eToColor (val) {
      return utils.CO2eToColor(val);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
