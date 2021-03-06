import Vue from 'vue';
import Vuex from 'vuex';

import backendUtils from '../../js/backend-utils';
// import Graph from '../../js/models/graph'; // path needs to be fixed
import graphTypes from '../../js/models/graph-types'; // path needs to be fixed

Vue.use(Vuex);

export default {
  namespaced: true,
  state: {
    graphs: []
  },
  getters: {
    getGraphsByBoardId: state => id => {
      return state.graphs
        .filter(graph => graph.refBoard === id)
        .sort((a, b) => a.order - b.order);
    }
  },
  mutations: {
    addGraph: function (state, payload) {
      state.graphs.push(payload.graph);
    },
    logout: function (state) {
      Vue.set(state, 'graphs', []);
    }
  },
  actions: {
    addGraphsByBoard: function ({ dispatch }, payload) {
      backendUtils
        .getEntity('?type=Graph&q=refBoard==' + payload.board.id)
        .then(response => {
          dispatch('addGraphs', { graphs: response.data });
        });
    },
    addGraphs: function ({ dispatch }, payload) {
      payload.graphs.forEach((graph, i) => {
        dispatch('addGraph', { graph: graph });
      });
    },
    addGraph: function ({ commit }, payload) {
      const graph = graphTypes(payload.graph.refGraphType);
      const promiseArray = [];
      // graph.values = payload.graph.connectedData;
      graph.endpoints(payload.graph.connectedData).forEach((ep, i) => {
        // if (ep) {
        promiseArray.push(
          backendUtils.getEntity(ep).then(response => {
            graph.values[i] = response.data;
          })
        );
        /* } else {
          graph.values[i] = payload.graph.connectedData[i];
        } */
      });

      payload.graph.endpointData = graph;

      Promise.all(promiseArray).then(values => {
        commit('addGraph', { graph: payload.graph });
      });
    }
  }
};
