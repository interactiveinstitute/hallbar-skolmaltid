import Vue from 'vue';
import Vuex from 'vuex';

import backendUtils from '../../js/backend-utils'; // path needs to be fixed
import User from '../../js/models/user'; // path needs to be fixed
import School from '../../js/models/school'; // path needs to be fixed

Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    user: new User(),
    school: new School()
  },
  getters: {

  },
  mutations: {
    setUser: function (state, payload) {
      // state.user = payload.user;
      state.user.init(payload.user);
    },
    setSchool: function (state, payload) {
      // state.school = payload.school;
      state.school.init(payload.school);
    }
  },
  actions: {
    getUserById: function ({ dispatch, commit }, payload) {
      backendUtils.getEntity(payload.idUser).then((response) => {
        commit('setUser', { user: response.data });
        dispatch('getSchoolById', { idSchool: response.data.refSchool.value });
        dispatch('charts/initByUser', { user: response.data }, { root: true });
      });
    },
    getSchoolById: function ({ commit }, payload) {
      backendUtils.getEntity(payload.idSchool).then((response) => {
        commit('setSchool', { school: response.data });
      });
    }
  }
};
