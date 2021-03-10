<template>
  <q-page class="">
    <h1>Välkommen {{ user.givenName }}!</h1>
    <p>
      Du är inloggad som testanvändare {{ user.givenName }} {{ user.familyName }}.
    </p>
    <p>
      I denna portal kan du som arbetar i skolkök se vilka elever som har
      anmält frånvaro och ifall dessa äter specialkost.
    </p>
    <p>
      Du kan se anmäld frånvaro och beräknad närvaro för dagens såväl som
      framtida datum.
    </p>
    <img src="~assets/graphics/Scenario_Attendance.png">
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

<style scoped lang="scss">
img {
  max-width: 100%;
  height: auto;
}
</style>
