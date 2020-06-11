<template>
  <q-page class="">
    <div>
      <h2>Svinnfinity 🍛</h2>
      <!--RestTest /-->
      <Graph :data="data" />
    </div>
  </q-page>
</template>

<script>
// import RestTest from 'components/RestTest.vue';
import Graph from 'components/Chart.vue';

import data from 'assets/data/dummy.json';

export default {
  name: 'PageIndex',
  components: {
    // RestTest,
    Graph
  },
  data: function () {
    return {
      data: data
    };
  }
};
</script>
