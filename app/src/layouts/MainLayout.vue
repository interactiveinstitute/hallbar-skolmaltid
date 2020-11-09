<template>
  <q-layout view="lHh Lpr lFf">
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
          Inloggad som:
          <strong>
            <br>
            {{ user.givenName }} {{ user.familyName }}
            <br>
            <div v-for="(school, i) in schools" :key="i">
              {{ school.name }}
            </div>
          </strong>
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

import EssentialLink from 'components/EssentialLink';

export default {
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  data () {
    return {
      leftDrawerOpen: false,
      essentialLinks: [
        {
          title: 'Hem',
          icon: 'home',
          routeName: 'Home'
        },
        {
          title: 'Logga in (test)',
          icon: 'settings',
          routeName: 'Login'
        },
        {
          title: 'Mina bräden',
          // caption: 'Se alla bräden',
          icon: 'apps',
          routeName: 'Dashboard'
        },
        {
          title: 'Inställningar',
          // caption: 'Se och ändra inställningar',
          icon: 'settings',
          routeName: 'Settings'
        }
      ]
    };
  },
  computed: {
    ...mapState('user', ['user', 'schools'])
  }
};
</script>

<style scoped lang="scss">
.q-page {
  padding: 0 20px 0 20px;
}
</style>
