<template>
  <div id="q-app">
    <router-view class="text-body1" />
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted: function () {
    /* this.$store.dispatch('user/setUserById', {
      idUser: 'urn:ngsi-ld:Person:user1'
    }); */
  }
};
</script>

<style lang="scss">
@import './assets/style/layout.scss';
@import './assets/style/text.scss';
@import './assets/style/elements.scss';
@import './assets/style/classes.scss';
</style>
