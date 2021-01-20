import Graph from './graph';

import GraphType1 from 'components/graphTypes/GraphType1.vue';
import GraphTypeAttendanceDay from 'components/graphTypes/GraphTypeAttendanceDay.vue';
import GraphTypeAbsenceCalendar from 'components/graphTypes/GraphTypeAbsenceCalendar.vue';
import GraphTypeAbsenceLines from 'components/graphTypes/GraphTypeAbsenceLines.vue';
import GraphTypeAttendanceLongterm from 'components/graphTypes/GraphTypeAttendanceLongterm.vue';

// Add graphs in the graphTypes object
// Maps graph name to vue component
const graphTypes = {
  graphType1: GraphType1,
  graphTypeAttendanceDay: GraphTypeAttendanceDay,
  graphTypeAbsenceCalendar: GraphTypeAbsenceCalendar,
  graphTypeAbsenceLines: GraphTypeAbsenceLines,
  graphTypeAttendanceLongterm: GraphTypeAttendanceLongterm
};

export default function (type) {
  const graph = new Graph();
  graph.endpoints = graphTypes[type].methods.endpoints;
  return graph;
}
