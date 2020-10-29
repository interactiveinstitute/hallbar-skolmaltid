<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted: function () {
    this.$store.dispatch('user/setUserById', { idUser: 'user1' });
  }
};
</script>

<style lang="scss">
@import './assets/style/text.scss';
</style>
