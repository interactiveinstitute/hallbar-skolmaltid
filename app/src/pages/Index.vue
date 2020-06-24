<template>
  <q-page class="">
    <div>
      <!--h2>Svinnfinity 🍛</h2-->
      <!--RestTest /-->
      <Board />
    </div>
  </q-page>
</template>

<script>
// import RestTest from 'components/RestTest.vue';
import Board from 'components/Board.vue';

// import data from 'assets/data/dummy.json';

export default {
  name: 'PageIndex',
  components: {
    // RestTest,
    Board
  },
  data: function () {
    return {
      // data: data.board
    };
  }
};
</script>
