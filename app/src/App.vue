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
