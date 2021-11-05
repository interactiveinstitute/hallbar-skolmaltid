<template>
  <div class="BoardThumb">
    <router-link :to="{ name: 'AppBoard', params: { id: board.id } }" class="undecorated">
      <div>
        <h2 class="text-white">
          {{ board.name }}
        </h2>
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
  background: $primary;
  padding: 10px;
}

.BoardThumb:hover{
  background: $blue-7;
}

</style>
