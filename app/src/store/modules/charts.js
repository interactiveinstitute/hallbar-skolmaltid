import Vue from 'vue';
import Vuex from 'vuex';

import backendUtils from '../../js/backend-utils';
import Chart from '../../js/models/chart'; // path needs to be fixed
import chartTypes from '../../js/models/chart-types'; // path needs to be fixed

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
      // TODO: iterate over all user charts in all user boards

      // dummy chart for attendance: should be fetched from database
      const chartData = {
        type: 'attendance',
        attached: ['school1']
      };

      // const chart = new chartTypes[chartData.type]();
      const chart = chartTypes(chartData.type);

      const promiseArray = [];
      chart.endpoints(chartData.attached).forEach((ep, i) => {
        promiseArray.push(
          backendUtils.getEntity(ep).then((response) => {
            chart.values.push(response.data[i]);
          })
        );
      });

      Promise.all(promiseArray).then((values) => {
        commit('addChart', { chart: chart });
      });
    }
  }
};
