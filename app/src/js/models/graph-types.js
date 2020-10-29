import Graph from './graph';

export default function (type) {
  const graph = graphTypes[type]();
  graph.type = type;
  return graph;
}

// Define graphs and add to graphTypes object at the bottom of the file
// Each graph must return a Graph object

const graphType1 = function () {
  const graph = new Graph();
  graph.endpoints = attached => {
    return [];
  };
  return graph;
};

const graphTypeSchoolAttendance = function () {
  const graph = new Graph();
  /* graph.endpoints = attached => {
    return [
      null,
      '?type=SchoolAttendanceObserved&q=refSchool==' +
        attached[1] +
        '&limit=1&orderBy=!dateObserved'
    ];
  }; */
  graph.endpoints = attached => {
    return [
      attached[1],
      '?type=SchoolAbsenceReported&q=refSchool==' + attached[1],
      '?type=DietGroup&q=refSchool==' + attached[1]
    ];
  };
  return graph;
};

// Add graphs in the graphTypes object
const graphTypes = {
  graphType1,
  graphTypeSchoolAttendance
};
