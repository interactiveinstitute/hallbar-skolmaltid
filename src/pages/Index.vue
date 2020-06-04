<template>
  <q-page class="flex flex-center">
    <div>
      <h2>Svinnfinity 🍛♾️</h2>
      <RestTest></RestTest>
    </div>
  </q-page>
</template>

<script>

import RestTest from 'components/RestTest.vue' // why is @ not src? @/components/... does not work.

export default {
  name: 'PageIndex',
  components: {
    RestTest
  }
}
</script>
