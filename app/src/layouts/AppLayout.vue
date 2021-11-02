<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Hållbar skolmåltid
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label header class="text-grey-8">
          <p>
            <strong> {{ user.givenName }} {{ user.familyName }} </strong>
          </p>

          <SchoolSelect />
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view class="q-page" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { mapState } from 'vuex';

import SchoolSelect from 'components/SchoolSelect';
import EssentialLink from 'components/EssentialLink';

export default {
  name: 'MainLayout',
  components: {
    SchoolSelect,
    EssentialLink
  },
  data () {
    return {
      leftDrawerOpen: false,
      essentialLinks: [
        {
          title: 'Hem',
          icon: 'home',
          routeName: 'AppHome'
        },
        {
          title: 'Mina bräden',
          // caption: 'Se alla bräden',
          icon: 'apps',
          routeName: 'AppBoards'
        },
        {
          title: 'Inställningar',
          // caption: 'Se och ändra inställningar',
          icon: 'settings',
          routeName: 'AppSettings'
        },
        {
          title: 'Logga ut',
          // caption: 'Se och ändra inställningar',
          icon: 'exit_to_app',
          routeName: 'Logout'
        }
      ]
    };
  },
  preFetch ({ store, redirect }) {
    if (!store.getters['user/isLoggedIn']) {
      redirect({ path: '/' });
    }
  },
  computed: {
    ...mapState('user', ['user', 'schools', 'schoolSelectedId'])
  },
  created: function () {
    this.$store.dispatch('user/initUserByAuth');
  }
};
</script>

<style scoped lang="scss">
.q-page {
  padding: 0 20px 0 20px;
}
</style>
