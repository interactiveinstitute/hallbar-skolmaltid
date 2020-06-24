export default function (chartInit) {
  // reactive data
  const data = {
    type: '',
    values: [],
    name: ''
    // attached: []
  };

  if (chartInit) {
    init(chartInit);
  }

  function init (chartData) {
    data.type = chartData.type;
    // data.attached = chartData.attached;
  }

  return {
    data: data,
    init: init
  };
}
