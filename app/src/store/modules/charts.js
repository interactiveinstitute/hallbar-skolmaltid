import Vue from 'vue';
import Vuex from 'vuex';

import backendUtils from '../../js/backend-utils';
import Chart from '../../js/models/chart'; // path needs to be fixed

Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    charts: []
  },
  getters: {
  },
  mutations: {
    addChart: function (state, payload) {
      state.charts.push(payload.chart);
    }
  },
  actions: {
    initByUser: function ({ commit }, payload) {
      // iterate over all user charts in all user boards
      // dummy chart for attendance
      const chart = new Chart();
      chart.data.type = 'attendance';
      chart.data.name = 'Närvaro och frånvaro';
      backendUtils.getEntity('?type=SchoolAttendance&refSchool=' + payload.user.refSchool.value).then((response) => {
        chart.data.values.push(response.data[0]);
        commit('addChart', { chart: chart });
      });
    }
  }
};
