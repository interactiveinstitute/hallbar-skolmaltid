<template>
  <q-page class="">
    <h1>Välkommen {{ user.givenName }}!</h1>
  </q-page>
</template>

<script>
import backendUtils from '../js/backend-utils';
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
  },
  mounted: function () {
    backendUtils.getAllData();
  }
};
</script>
