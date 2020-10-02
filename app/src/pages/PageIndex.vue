<template>
  <q-page class="">
    <pre>
      {{ user }}
    </pre>
  </q-page>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'PageIndex',
  components: {},
  data: function () {
    return {
      // data: data.board
    };
  },
  computed: {
    ...mapState('user', ['user'])
  }
};
</script>
