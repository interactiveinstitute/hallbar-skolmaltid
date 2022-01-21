<template>
  <q-page class="">
    <div>
      <h2>Mina bräden</h2>

      <p>
        Här är alla dina bräden, kopplade till din användare.
      </p>
      <p>
        Ett bräde är en samling grafer eller annan typ av information.
      </p>

      <div class="boards">
        <BoardThumb v-for="(board, i) in boards" :key="i" :board="board" />
      </div>

      <p class="bg-grey-4 q-pa-md">
        <q-icon name="info" color="primary" size="sm" />
        I en framtida app kan du själv strukturera bräden, grafer och annat innehåll efter egna behov och önskemål.
      </p>
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
