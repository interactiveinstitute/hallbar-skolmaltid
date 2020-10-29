import Graph from './graph';

import GraphType1 from 'components/graphTypes/graphType1.vue';
import GraphTypeSchoolAttendance from 'components/graphTypes/graphTypeSchoolAttendance.vue';
import GraphTypeAbsenceCalendar from 'components/graphTypes/GraphTypeAbsenceCalendar.vue';

// Add graphs in the graphTypes object
// Maps graph name to vue component
const graphTypes = {
  graphType1: GraphType1,
  graphTypeSchoolAttendance: GraphTypeSchoolAttendance,
  graphTypeAbsenceCalendar: GraphTypeAbsenceCalendar
};

export default function (type) {
  const graph = new Graph();
  graph.endpoints = graphTypes[type].methods.endpoints;
  graph.type = type;
  return graph;
}
