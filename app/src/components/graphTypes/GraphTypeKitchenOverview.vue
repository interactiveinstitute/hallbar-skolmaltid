<template>
  <div v-if="graph.endpointData" class="GraphTypeKitchenOverview">
    <!--p class="text-grey-10">
      Meny för {{ schoolSelected.name }} {{ datesSelectedWeek[0] }} - {{ datesSelectedWeek[4] }}.
    </p-->

    <q-table
      :columns="columns"
      :data="rows"
      row-key="date"
      title-class="text-body2 text-bold"
      table-header-class="info"
      :rows-per-page-options="[0]"
      hide-pagination
    >
      <template v-slot:body="props">
        <q-tr :props="props" class="cursor-pointer" :class="{'bg-grey-3': props.row.date === dateToday && props.row.date !== dateSelected, 'bg-blue-2': props.row.date === dateSelected} " @click="onRowClick(props.row)">
          <q-td key="date" :props="props">
            {{ props.row.date }}
          </q-td>
          <q-td key="name" :props="props" class="text-bold">
            <span v-if="props.row.name">{{ props.row.name }}</span>
            <span v-else class="text-italic text-grey-8">
              Ingen mat planerad
            </span>
          </q-td>
          <q-td key="allergens" :props="props" class="text-negative">
            {{ props.row.allergens }}
          </q-td>
          <q-td key="kcal" :props="props">
            {{ props.row.kcal }}
          </q-td>
          <q-td key="co2" :props="props">
            <q-chip v-if="props.row.co2" :color="props.row.co2 > 0.5 ? 'negative' : 'positive'" text-color="white" dense>
              {{ props.row.co2 }}
            </q-chip>
          </q-td>
          <q-td key="waste" :props="props">
            {{ props.row.waste }}
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import { subDays, addDays } from 'date-fns';
// import backendUtils from '../../js/backend-utils';
// import Chart from 'chart.js'; // NOTE! npm package Chart.js

export default {
  name: 'GraphTypeKitchenOverview',
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
      columns: [
        { name: 'date', label: 'Datum', field: 'date', align: 'left' },
        { name: 'name', label: 'Måltid', field: 'name', align: 'left' },
        { name: 'allergens', label: 'Allergener', field: 'allergens', align: 'left' },
        { name: 'kcal', label: 'Energi (kcal)', field: 'kcal', align: 'left' },
        { name: 'co2', label: 'Klimatavtryck (kg CO2e)', field: 'co2', align: 'left' },
        { name: 'waste', label: 'Matsvinn (g/person)', field: 'waste', align: 'left' }
      ]
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
    datesSelectedWeek () {
      var datesW = [];
      var date = new Date(this.dateSelected);
      var monday = subDays(date, date.getDay() > 0 ? date.getDay() - 1 : 6);
      for (var i = 0; i < 5; i++) {
        datesW[i] = addDays(monday, i).toLocaleDateString();
      }
      return datesW;
    },
    waste () {
      return this.graph.endpointData.values[2];
    },
    rows () {
      return this.datesSelectedWeek.map(d => {
        const row = {
          date: d
        };
        const m = this.meals.find(m => m.date.substring(0, 10) === d);
        if (m) {
          row.name = m.courses[0].name;
          row.allergens = m.courses[0].possibleAllergens.join(', ');
          row.kcal = m.courses[0].nutrients.find(n => n.unit === 'kcal').amount;
          row.co2 = m.courses[0].co2Equivalents;
        }
        const w = this.waste.find(w => w.date.substring(0, 10) === d);
        if (w) {
          row.waste = Math.round((parseFloat(w.kitchenWaste) + parseFloat(w.plateWaste) + parseFloat(w.servingWaste)) * 1000 * 100) / 100;
        }
        return row;
      });
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
        '?type=OpenMeal&q=refSchool==' + endpointDataRequest.school + '&limit=1000',
        '?type=FoodWaste&q=refSchool==' + endpointDataRequest.school + '&limit=1000'
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
    onRowClick (row) {
      this.$store.commit('user/selectDate', { date: row.date });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
