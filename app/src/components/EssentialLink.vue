<template>
  <q-item clickable tag="router-link" :to="{name: routeName}">
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
      <q-item-label caption>
        {{ caption }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>

// import { QSideLink } from quasar

export default {
  name: 'EssentialLink',
  components: {
    // QSideLink
  },
  props: {
    title: {
      type: String,
      required: true
    },

    caption: {
      type: String,
      default: ''
    },

    routeName: {
      type: String,
      default: ''
    },

    icon: {
      type: String,
      default: ''
    }
  }
};
</script>
