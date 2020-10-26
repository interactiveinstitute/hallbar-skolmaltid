<template>
  <q-page class="">
    <div>
      <h2>Översikt</h2>

      <p>
        Här är alla dina bräden för skolkök, lärare, elever och föräldrar.
      </p>

      <div class="boards">
        <BoardThumb v-for="(board, i) in boards" :key="i" :board="board" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapState } from 'vuex';
import BoardThumb from 'components/BoardThumb.vue';

export default {
  name: 'PageDashboard',
  components: { BoardThumb },
  props: {},
  computed: {
    ...mapState('boards', ['boards'])
  },
  mounted: function () {},
  methods: {}
};
</script>

<style scoped lang="scss">
.boards {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: flex-start;
}

.boards > * {
  margin: 5px;
}
</style>
