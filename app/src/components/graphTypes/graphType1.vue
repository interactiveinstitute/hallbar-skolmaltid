<template>
  <div class="GraphType1">
    <h4>Graftyp 1</h4>
    <p>
      Det här en graftyp som är ganska intetsägande. Men den visar att det går
      att skapa olika typer av datapresentationer.
    </p>
    <p>
      Användarens egeninlagda data:
    </p>
    <div v-for="sd in graph.chart.staticData(graph.chart.values)" :key="sd">
      {{ sd }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'GraphType1',
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
    return {};
  },
  computed: {},
  mounted: function () {},
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.GraphType1 {
}
</style>
