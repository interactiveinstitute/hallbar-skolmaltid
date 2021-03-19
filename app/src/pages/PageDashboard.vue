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
      <p>
        Du själv kan strukturera brädena och innehållet efter dina egna önskemål och behov, t.ex. för att visa flera grafer på en och samma skärm i skolköket - utan att behöva klicka runt.
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
