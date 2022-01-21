<template>
  <q-page class="PageHome">
    <div class="padding">
      <h2>Gör elevnärvaron synlig i skolköket</h2>
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

.border{
  border: 1px solid gray;
}

</style>
