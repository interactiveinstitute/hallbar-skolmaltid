export default function (schoolInit) {
  if (schoolInit) {
    init(schoolInit);
  }

  // reactive data
  const data = {
    name: '',
    logo: ''
  };

  function init (school) {
    data.name = school.name.value;
    data.logo = school.logo.value;
  }

  return {
    data: data,
    init: init
  };
}
