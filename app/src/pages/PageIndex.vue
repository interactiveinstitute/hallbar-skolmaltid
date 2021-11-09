<template>
  <q-page class="">
    <h1>Välkommen {{ user.givenName }}!</h1>

    <p class="q-mb-md">
      <span class="info q-pa-md">
        Du är inloggad som testanvändare {{ user.givenName }} {{ user.familyName }}.
      </span>
    </p>
    <p>
      I denna portal kan du som arbetar i skolkök se vilka elever som har
      anmält frånvaro och ifall dessa äter specialkost.
    </p>
    <p>
      Du kan även se menyn för dagen eller för veckan samt allergener, energi, klimatavtryck, näringsinnehåll och matsvinn för varje rätt.
    </p>

    <q-img src="~assets/graphics/Scenario_Attendance.png" class="border">
      <div class="absolute-bottom text-center">
        Se anmäld frånvaro och planera skolmåltiderna därefter. En av flera funktioner i portalen.
      </div>
    </q-img>
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

.border{
  border: 1px solid gray;
}

</style>
