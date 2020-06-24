import Chart from './chart';

// Define new charts below
// Each chart must return a Chart object

const attendance = function () {
  const chart = new Chart();

  chart.type = 'attendance';
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

export default {
  attendance
};
