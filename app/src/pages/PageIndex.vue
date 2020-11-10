<template>
  <q-page class="">
    <h1>Välkommen {{ user.givenName }}!</h1>
    <!--pre>
      {{ user }}
    </pre-->
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
  /* preFetch ({ store, redirect }) {
    if (!store.getters['user/isLoggedIn']) {
      redirect({ path: '/' });
    }
  }, */
  computed: {
    ...mapState('user', ['user'])
  }
};
</script>
