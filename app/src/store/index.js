import Vue from 'vue';
import Vuex from 'vuex';

import user from './modules/user.js';
import boards from './modules/boards.js';
import graphs from './modules/graphs.js';

Vue.use(Vuex);

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default (function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      user: user,
      boards: boards,
      graphs: graphs
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  });

  return Store;
});
