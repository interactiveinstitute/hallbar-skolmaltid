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
    },
    setGraphData (state, payload) {
      Vue.set(payload.graph, 'endpointData', payload.data);
      // payload.graph.endpointData = payload.data;
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
    addGraphs: function ({ commit }, payload) {
      payload.graphs.forEach((graph, i) => {
        commit('addGraph', { graph: graph });
      });
    },
    setGraphData ({ state, commit }, payload) {
      console.log('SET GRAPH DATA', payload.graph);
      const graph = graphTypes(payload.graph.refGraphType);
      const promiseArray = [];
      graph.endpoints(payload.endpointDataRequest).forEach((ep, i) => {
        console.log(ep);
        promiseArray.push(
          backendUtils.getEntity(ep).then(response => {
            graph.values[i] = response.data;
          })
        );
      });
      Promise.all(promiseArray).then(values => {
        commit('setGraphData', { graph: payload.graph, data: graph });
      });
    }
  }
};
