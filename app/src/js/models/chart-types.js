import ChartTypedBase from './chart-typed-base'; // path needs to be fixed

const attendance = function () {
  const chartTyped = new ChartTypedBase();

  chartTyped.name = 'Närvaro och frånvaro';
  chartTyped.attachmentTypes = ['School'];

  chartTyped.endpoints = (attached) => {
    return [
      '?type=SchoolAttendance&refSchool=' + attached[0]
    ];
  };

  chartTyped.chartJSData = (values) => {
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

  return chartTyped;
};

export default {
  attendance
};
