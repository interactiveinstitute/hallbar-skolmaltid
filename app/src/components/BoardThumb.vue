<template>
  <div class="BoardThumb">
    <router-link :to="{ name: 'Board', params: { id: board.id } }">
      <div>
        <h4>{{ board.id }}</h4>
      </div>
    </router-link>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'ComponentTemplate',
  components: {},
  props: { board: Object },
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
.BoardThumb {
  display: flex;
  background: lightgray;
  padding: 10px;
}
</style>
