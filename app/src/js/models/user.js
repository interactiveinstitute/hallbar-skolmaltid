export default function (userInit) {
  // reactive data
  const data = {
    givenName: '',
    familyName: ''
  };

  if (userInit) {
    init(userInit);
  }

  function init (user) {
    data.givenName = user.givenName.value;
    data.familyName = user.familyName.value;
  }

  return {
    data: data,
    init: init
  };
}
