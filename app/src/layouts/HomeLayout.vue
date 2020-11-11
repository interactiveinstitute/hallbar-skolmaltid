<template>
  <q-layout view="hHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
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
          <Login />
        </q-item-label>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import Login from 'components/Login.vue';

export default {
  components: {
    Login
  },
  data () {
    return {
      msgError: '',
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
  }
};
</script>
