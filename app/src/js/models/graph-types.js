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

  graph.name = 'Graph1';
  graph.attachmentTypes = ['Text'];

  graph.endpoints = attached => {
    return [null];
  };

  graph.staticData = values => {
    return [values[0]];
  };

  graph.chartJSData = values => {
    return null;
  };

  return graph;
};

const graphTypeSchoolAttendance = function () {
  const graph = new Graph();

  graph.name = 'Närvaro och frånvaro';
  graph.attachmentTypes = ['School'];

  graph.endpoints = attached => {
    return ['?type=SchoolAttendance&refSchool=' + attached[0]];
  };

  graph.staticData = values => {
    return [];
  };

  graph.chartJSData = values => {
    return {
      type: 'bar',
      data: {
        labels: ['Närvarande', 'Frånvarande'],
        datasets: [
          {
            data: [
              values[0].attendance.value.present.value,
              values[0].attendance.value.absent.value
            ],
            backgroundColor: [
              'rgba(99, 255, 132, 0.2)',
              'rgba(255, 99, 132, 0.2)'
            ],
            borderWidth: 1
          }
        ]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };
  };

  return graph;
};

// Add graphs in the graphTypes object
const graphTypes = {
  graphType1,
  graphTypeSchoolAttendance
};
