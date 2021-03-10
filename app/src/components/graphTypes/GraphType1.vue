<template>
  <div class="GraphType1">
    <h4>Vad skulle du vilja se här?</h4>
    <p>
      Här är det än så länge tomt. Men vi visar härmed att det går
      att skapa olika bräden med olika typ av information.
    </p>
    <p>
      Vad skulle du vilja visades här? Data om matsvinn, klimatavtryck eller något helt annat?
    </p>

    <!--form @submit.prevent="changeValue">
      <input name="value" type="text" placeholder="Ange nytt värde">
      <button type="submit">
        Uppdatera värde
      </button>
    </form-->
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
    endpoints: function (attached) {
      // Required method for all graph types
      return [];
    },
    changeValue: function (event) {
      this.$store.commit('setValue', {
        object: this.graph.connectedData,
        index: 0,
        value: event.target.elements.value.value
      });
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
