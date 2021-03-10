<template>
  <q-page class="" />
</template>

<script>
// import backendUtils from '../js/backend-utils';

// import { mapState } from 'vuex';

export default {
  name: 'PageLogout',
  created: function () {
    this.$store.dispatch('user/logout');
    this.$router.push({ name: 'Home' });
  }
};
</script>
