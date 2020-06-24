const attendance = function () {
  const name = 'Närvaro och frånvaro';
  const attachmentTypes = ['School'];

  function endpoints (attached) {
    return [
      '?type=SchoolAttendance&refSchool=' + attached[0]
    ];
  }
  function chartJSData (values) {
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
  }

  return {
    name: name,
    attachmentTypes: attachmentTypes,
    endpoints: endpoints,
    chartJSData: chartJSData
  };
};

export default {
  attendance
};
