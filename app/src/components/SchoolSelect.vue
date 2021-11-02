<template>
  <div class="SchoolSelect">
    <q-select v-model="selectedId" :options="schoolsSelect" emit-value />
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
// import ComponentName from '@/components/ComponentName.vue'

export default {
  name: 'SchoolSelect',
  components: {
    // ComponentName
  },
  props: {
    // value: Number
  },
  data: function () {
    return {
      // name: "My Name"
    };
  },
  computed: {
    ...mapState('user', ['schools', 'schoolSelectedId']),
    ...mapGetters('user', ['schoolSelected']),
    selectedId: {
      get () {
        return this.schoolsSelect.find(s => s.value === this.$store.state.user.schoolSelectedId);
      },
      set (value) {
        this.$store.commit('user/selectSchoolId', { id: value });
      }
    },
    schoolsSelect () {
      return this.schools.map(s => { return { label: s.name, value: s.id }; });
    }
  },
  mounted: function () {
    console.log(this.$store);
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.ComponentTemplate {
}
</style>
