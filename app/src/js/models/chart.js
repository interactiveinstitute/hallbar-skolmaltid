export default function (chartInit) {
  // reactive data
  const data = {
    type: '',
    values: [],
    name: ''
  };

  if (chartInit) {
    init(chartInit);
  }

  function init (chartData) {
    data.type = chartData.type;
  }

  return {
    data: data,
    init: init
  };
}
