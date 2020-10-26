<template>
  <div class="Board">
    <div>
      <h3>{{ board.name }}</h3>
      <div class="boards">
        <div v-for="(graph, i) in graphs" :key="i">
          <component :is="graph.refGraphType" :graph="graph" />
          <!--pre>
            {{ graph }}
          </pre-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
// import Graph from 'components/Graph.vue';
import graphType1 from 'components/graphTypes/graphType1.vue';
import GraphTypeSchoolAttendance from 'components/graphTypes/graphTypeSchoolAttendance.vue';

export default {
  name: 'ComponentTemplate',
  components: {
    // Graph,
    graphType1,
    GraphTypeSchoolAttendance
  },
  props: {
    board: Object
  },
  data: function () {
    return {
      // name: "My Name"
    };
  },
  computed: {
    // ...mapState('graphs', ['graphs']),
    ...mapGetters('graphs', ['getGraphsByBoardId']),
    graphs: function () {
      return this.getGraphsByBoardId(this.board.id);
    }
  },
  mounted: function () {},
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.Board {
  display: flex;
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

.boards {
  display: flex;
  flex-wrap: wrap;
}

.boards > div {
  flex: 1 0 50%;
}
</style>
