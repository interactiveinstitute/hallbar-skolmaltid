<template>
  <q-page class="PageHome">
    <div class="padding">
      <h2>Gör elevnärvaron synlig i skolköket</h2>
      <p>
        I denna portal kan du som arbetar i skolkök se vilka elever som har
        anmält frånvaro och ifall dessa äter specialkost.
      </p>
      <p>
        Du kan se anmäld frånvaro och beräknad närvaro för dagens såväl som
        framtida datum.
      </p>
      <img src="~assets/graphics/Scenario_Attendance.png">
    </div>
  </q-page>
</template>

<script>
// import backendUtils from '../js/backend-utils';

export default {
  name: 'PageHome',
  components: {},
  data: function () {
    return {};
  },
  computed: {},
  methods: {}
};
</script>

<style scoped lang="scss">
.PageHome {
}

img {
  max-width: 100%;
  height: auto;
}
</style>
