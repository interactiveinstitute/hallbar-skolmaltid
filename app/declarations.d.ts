



// this files is to give us better autocomplete in vs code
// vs code uses typescript to calculate intellisense, also in non typescript projects



//Import vue so we can augment it
import Vue from 'vue';

import { AxiosStatic } from 'axios';

//This seems to give intellisense for 'this.$q...'
import quasar from 'quasar'


//Here we augment the vue class so we get intellisense on injected properties
declare module 'vue/types/vue' {
  interface Vue {
    $axios: AxiosStatic
  }
}