<template>
  <div class="GraphType1">
    <h4>Här är det än så länge tomt.</h4>
    <p>
      Vad skulle du vilja visades:
      <ul>
        <li>på skärmarna i skolans korridor?</li>
        <li>i lärarrummet?</li>
        <li>för skolkuratorn?</li>
        <li>osv.</li>
      </ul>
    </p>
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
