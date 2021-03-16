<template>
  <div class="Login">
    <h2>Logga in</h2>

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
          <input type="password" name="password" value="skolmat">
        </label>
      </p>
      <p>
        <button type="submit">
          Logga in
        </button>
      </p>
      <p v-if="msgError" class="info error">
        {{ msgError }}
      </p>
    </form>
  </div>
</template>

<script>
import backendUtils from '../js/backend-utils';

export default {
  name: 'Login',
  components: {},
  data: function () {
    return {
      msgError: ''
    };
  },
  computed: {},
  methods: {
    login: function (e) {
      const self = this;

      backendUtils
        .createKeyrockUserAccessToken(
          // Create Keyrock user access token
          e.target.elements.name.value,
          e.target.elements.password.value
        )
        // User access token received
        .then(self.userAccessTokenSuccess)
        // User Keyrock token received
        .then(self.keyrockTokenSuccess)
        // Keyrock user received
        .then(self.keyrockUserSuccess)
        .catch(self.onLoginError);
    },
    userAccessTokenSuccess: function (r) {
      this.$store.commit('user/setAuthKey', {
        key: 'access',
        value: r.response.data
      });
      backendUtils.setAxiosAuthToken(r.response.data.access_token); // Set Axios user access token
      return backendUtils.createKeyrockToken(
        // Create user Keyrock token
        r.loginDetails.name,
        r.loginDetails.password
      );
    },
    keyrockTokenSuccess: function (r) {
      this.$store.commit('user/setAuthKey', {
        key: 'keyrock_token',
        value: r.headers['x-subject-token']
      });
      return backendUtils.getKeyrockUser(r.headers['x-subject-token']); // Get Keyrock user
    },
    keyrockUserSuccess: function (r) {
      this.$store.commit('user/setAuthKey', {
        key: 'user',
        value: r.data.User
      });
      this.$router.push({ name: 'AppHome' });
    },
    onLoginError: function (e) {
      console.log('Error');
      this.msgError = 'Fel e-post eller lösenord. Försök igen.';
    }
  }
};
</script>

<style scoped lang="scss">
.Login {
}

img {
  max-width: 100%;
  height: auto;
}
</style>
