<template>
  <q-page class="">
    <div v-if="board">
      <Board :board="board" />
    </div>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex';
import Board from 'components/Board.vue';

export default {
  name: 'PageBoard',
  components: {
    // RestTest,
    Board
  },
  props: {},
  data: function () {
    return {};
  },
  computed: {
    ...mapGetters('boards', ['getBoardById']),
    board: function () {
      return this.getBoardById(this.$route.params.id);
    }
  },
  mounted: function () {},
  methods: {}
};
</script>
