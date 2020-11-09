<template>
  <q-page class="">
    <h2>Logga in</h2>
    <p>
      Denna sidan är endast för testsyfte. Givetvis ska ingen inloggningssida
      finnas i huvudmenyn.
    </p>
    <form @submit.prevent="login">
      E-post: <input type="text" name="name" value="user1@test.com">
      <br>
      Lösenord: <input type="text" name="password" value="test">
      <br>
      <button type="submit">
        Logga in
      </button>
    </form>
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
  computed: {
    ...mapState('user', ['user'])
  },
  methods: {
    login: function (e) {
      backendUtils.createKeyrockToken(
        event.target.elements.name.value,
        event.target.elements.password.value
      );
    }
  }
};
</script>
