<template>
  <div v-if="graph.endpointData" class="GraphTypeOpenMeal">
    <div class="info">
      <h2 class="text-white">
        Meny
      </h2>
      <p>
        Meny för {{ schoolSelected.name }} {{ dateSelected }}.
      </p>
    </div>
    <div v-if="mealSelectedDate" class="border q-pa-md">
      <div v-for="(course,iCourse) in mealSelectedDate.courses" :key="iCourse">
        <h3>{{ course.name }}</h3>
        <div class="row q-col-gutter-md">
          <div class="col">
            <h4>Ingredienser</h4>
            <ul>
              <li v-for="(ing,iIng) in course.ingredientsLabel.split(',')" :key="iIng">
                {{ ing }}
              </li>
            </ul>
          </div>
          <div class="col">
            <h4>Allergener</h4>
            <ul v-if="course.possibleAllergens.length" class="text-negative">
              <li v-for="(allergen,iAllergen) in course.possibleAllergens" :key="iAllergen">
                {{ allergen }}
              </li>
            </ul>
            <span v-else>Inga allergener</span>
          </div>
          <div class="col">
            <h4>Näringsämnen</h4>
            <div v-for="(nut, iNut) in course.nutrients" :key="iNut">
              <strong>{{ nut.name }}: </strong> {{ nut.amount }} {{ nut.unit }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      Menyn är ej planerad för {{ dateSelected }}.
    </div>

    <!--pre>
      {{ }}
    </pre-->
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
// import { format } from 'date-fns';
// import backendUtils from '../../js/backend-utils';
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
      chartTotal: undefined
    };
  },
  computed: {
    ...mapState('user', ['schoolSelectedId', 'dateSelected']),
    ...mapGetters('user', ['schoolSelected']),
    meals () {
      return this.graph.endpointData.values[1];
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
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
