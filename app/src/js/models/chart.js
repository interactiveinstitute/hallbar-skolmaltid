export default function (chartInit) {
  if (chartInit) {
    init(chartInit);
  }

  // reactive data
  const data = {
    type: '',
    values: []
  };

  function init (chart) {
  }

  return {
    data: data,
    init: init
  };
}
