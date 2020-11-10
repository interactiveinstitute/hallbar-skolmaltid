<template>
  <q-page class="PageLogin">
    <div>
      <h1>Logga in</h1>
      <form @submit.prevent="login">
        <p>
          <label>
            E-post
            <br>
            <input type="text" name="name" value="user1@test.com">
          </label>
        </p>
        <p>
          <label>
            Lösenord
            <br>
            <input type="password" name="password" value="test">
          </label>
        </p>
        <p>
          <button type="submit">
            Logga in
          </button>
        </p>
      </form>
      <!--pre>
      {{ auth }}
    </pre>
    <pre>
      {{ user }}
    </pre-->
    </div>
  </q-page>
</template>

<script>
import backendUtils from '../js/backend-utils';

import { mapState } from 'vuex';

export default {
  name: 'PageLogin',
  components: {},
  data: function () {
    return {
      // data: data.board
    };
  },
  computed: {
    ...mapState('user', ['auth', 'user'])
  },
  methods: {
    login: function (e) {
      const self = this;

      backendUtils
        .createKeyrockAccessToken(
          // Create user access token
          e.target.elements.name.value,
          e.target.elements.password.value
        )
        // User access token received
        .then(function (r) {
          console.log(r);
          self.$store.commit('user/setAuthKey', {
            key: 'access',
            value: r.data
          });
          backendUtils.setAxiosAuthToken(r.data.access_token); // Set Axios user access token
          return (
            backendUtils
              .createKeyrockToken(
                // Create user Keyrock token
                e.target.elements.name.value,
                e.target.elements.password.value
              )
              // User Keyrock token received
              .then(function (r) {
                console.log(r);
                self.$store.commit('user/setAuthKey', {
                  key: 'keyrock_token',
                  value: r.headers['x-subject-token']
                });
                return backendUtils.getKeyrockUser(
                  r.headers['x-subject-token']
                ); // Get Keyrock user
              })
              // Keyrock user received
              .then(function (r) {
                console.log(r);
                self.$store.commit('user/setAuthKey', {
                  key: 'user',
                  value: r.data.User
                });
                self.$router.push({ name: 'AppHome' });
              })
          );
        });
    }
  }
};
</script>

<style scoped lang="scss">
.PageLogin {
  display: flex;
  justify-content: center;
}
</style>
