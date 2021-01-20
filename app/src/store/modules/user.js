import Vue from 'vue';
import Vuex from 'vuex';

import backendUtils from '../../js/backend-utils'; // path needs to be fixed
// import User from '../../js/models/user'; // path needs to be fixed
// import School from '../../js/models/school'; // path needs to be fixed

Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    auth: {},
    user: {},
    schools: []
  },
  getters: {
    getAuth: state => {
      return state.auth;
    },
    isLoggedIn: state => {
      return state.auth.access;
    }
  },
  mutations: {
    setAuthKey: function (state, payload) {
      Vue.set(state.auth, payload.key, payload.value);
      // state.auth.[payload.key] = payload.value;
    },
    setUser: function (state, payload) {
      // state.user = payload.user;
      state.user = payload.user;
    },
    addSchool: function (state, payload) {
      // state.school = payload.school;
      state.schools.push(payload.school);
    },
    logout: function (state) {
      Vue.set(state, 'auth', {});
      Vue.set(state, 'user', {});
      Vue.set(state, 'schools', []);
    }
  },
  actions: {
    initUserByAuth: function ({ state, dispatch }, payload) {
      dispatch('setUserById', { idUser: state.auth.user.id });
    },
    setUserById: function ({ dispatch, commit }, payload) {
      backendUtils.getEntity(payload.idUser).then(response => {
        commit('setUser', { user: response.data });
        dispatch('setSchoolsById', { schools: response.data.refSchool });
        // dispatch('graphs/initByUser', { user: response.data }, { root: true });
        dispatch(
          'boards/setBoardsByUser',
          { user: response.data },
          { root: true }
        );
      });
    },
    setSchoolsById: function ({ commit }, payload) {
      payload.schools.forEach((school, i) => {
        backendUtils.getEntity(school).then(response => {
          commit('addSchool', { school: response.data });
        });
      });
    },
    loggedInTest: function ({ state }) {
      return new Promise((resolve, reject) => {
        console.log(state.auth.auth);
        resolve(state.auth.auth);
      });
    }
  }
};
