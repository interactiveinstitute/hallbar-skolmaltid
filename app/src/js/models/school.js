export default function (schoolInit) {
  // reactive data
  const data = {
    name: '',
    logo: ''
  };

  if (schoolInit) {
    init(schoolInit);
  }

  function init (school) {
    data.name = school.name.value;
    data.logo = school.logo.value;
  }

  return {
    data: data,
    init: init
  };
}
