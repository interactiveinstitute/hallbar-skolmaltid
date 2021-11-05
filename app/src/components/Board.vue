<template>
  <div class="Board">
    <div>
      <h1>{{ board.name }}</h1>
      <div class="bg-white q-pt-md q-pb-md text-bold">
        <label>Datum: <input v-model="dateSelected" required type="date"> </label>
      </div>
      <div class="boards">
        <div v-for="(graph, i) in graphs" :key="i" class="of">
          <component :is="graph.refGraphType" :graph="graph" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
// import Graph from 'components/Graph.vue';
import graphType1 from 'components/graphTypes/GraphType1.vue';
import GraphTypeAttendanceDay from 'components/graphTypes/GraphTypeAttendanceDay.vue';
import GraphTypeAbsenceCalendar from 'components/graphTypes/GraphTypeAbsenceCalendar.vue';
import GraphTypeAbsenceLines from 'components/graphTypes/GraphTypeAbsenceLines.vue';
import GraphTypeAttendanceLongterm from 'components/graphTypes/GraphTypeAttendanceLongterm.vue';
import GraphTypeOpenMeal from 'src/components/graphTypes/GraphTypeOpenMeal.vue';
import GraphTypeFoodWaste from 'src/components/graphTypes/GraphTypeFoodWaste.vue';
import GraphTypeKitchenOverview from 'src/components/graphTypes/GraphTypeKitchenOverview.vue';

export default {
  name: 'ComponentTemplate',
  components: {
    // Graph,
    graphType1,
    GraphTypeAttendanceDay,
    GraphTypeAbsenceCalendar,
    GraphTypeAbsenceLines,
    GraphTypeAttendanceLongterm,
    GraphTypeOpenMeal,
    GraphTypeFoodWaste,
    GraphTypeKitchenOverview
  },
  props: {
    board: Object
  },
  data: function () {
    return {
    };
  },
  computed: {
    ...mapGetters('user', ['schoolSelected']),
    ...mapGetters('graphs', ['getGraphsByBoardId']),
    graphs: function () {
      return this.getGraphsByBoardId(this.board.id);
    },
    dateSelected: {
      get () {
        return this.$store.state.user.dateSelected;
      },
      set (value) {
        this.$store.commit('user/selectDate', { date: value });
      }
    }
  },
  mounted: function () {
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Board {
  display: flex;
  position: relative;
}

.Board > * {
  flex: 1;
}

pre {
  padding: 5px;
  background: rgb(240, 240, 240);
  border-left: 1px solid lightgray;
  margin: 10px;
}

.boards > div {
  flex: 1 0 50%;
  border: 0px solid rgb(240, 240, 240);
  margin-bottom: 10px;
}

.sticky {
  border-bottom: 0px solid dodgerblue;
}
</style>
