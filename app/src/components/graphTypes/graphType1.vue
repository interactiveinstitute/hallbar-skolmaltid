<template>
  <div class="GraphType1">
    <h4>Graftyp 1</h4>
    <p>
      Det här en graftyp som är ganska intetsägande. Men den visar att det går
      att skapa olika typer av datapresentationer.
    </p>
    <p>Användarens egeninlagda data: {{ graph.preparedData.values[0] }}</p>

    <form @submit.prevent="changeValue">
      <input name="value" type="text" placeholder="Ange nytt värde">
      <button type="submit">
        Uppdatera värde
      </button>
    </form>
  </div>
</template>

<script>
import backendUtils from '../../js/backend-utils';
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
  methods: {
    changeValue: function (event) {
      this.$store.commit('setValue', {
        object: this.graph.connectedData,
        index: 0,
        value: event.target.elements.value.value
      });
      this.$store.commit('setValue', {
        object: this.graph.preparedData.values,
        index: 0,
        value: event.target.elements.value.value
      }); // This should be made reactive
      backendUtils.updateAttribute(
        this.graph.id,
        'connectedData',
        this.graph.connectedData
      );
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.GraphType1 {
}
</style>
