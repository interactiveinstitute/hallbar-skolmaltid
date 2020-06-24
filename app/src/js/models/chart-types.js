import Chart from './chart';

export default function (type) {
  const chart = chartTypes[type]();
  chart.type = type;
  return chart;
};

// Define charts and add to chartTypes object at the bottom of the file
// Each chart must return a Chart object

const attendance = function () {
  const chart = new Chart();

  chart.name = 'Närvaro och frånvaro';
  chart.attachmentTypes = ['School'];

  chart.endpoints = (attached) => {
    return [
      '?type=SchoolAttendance&refSchool=' + attached[0]
    ];
  };

  chart.chartJSData = (values) => {
    return {
      type: 'bar',
      data: {
        labels: ['Närvarande', 'Frånvarande'],
        datasets: [
          {
            data: [values[0].attendance.value.present.value, values[0].attendance.value.absent.value],
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

  return chart;
};

// Add charts in the chartTypes object
const chartTypes = {
  attendance
};
