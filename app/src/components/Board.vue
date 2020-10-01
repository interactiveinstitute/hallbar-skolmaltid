<template>
  <div class="Board">
    <div>
      <h3>Mitt bräde</h3>
      <div v-for="(graph, i) in graphs" :key="i">
        <Graph :graph="graph" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Graph from 'components/Graph.vue';

export default {
  name: 'ComponentTemplate',
  components: {
    Graph
  },
  props: {},
  data: function () {
    return {
      // name: "My Name"
    };
  },
  computed: {
    ...mapState('graphs', ['graphs'])
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
</style>
