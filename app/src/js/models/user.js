export default function (userInit) {
  if (userInit) {
    init(userInit);
  }

  // reactive data
  const data = {
    givenName: '',
    familyName: ''
  };

  function init (user) {
    data.givenName = user.givenName.value;
    data.familyName = user.familyName.value;
  }

  return {
    data: data,
    init: init
  };
}
