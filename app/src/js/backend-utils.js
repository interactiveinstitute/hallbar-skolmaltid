import axios from 'axios';

const config = {
  keyrock: 'http://localhost:3005/v1/',
  keyrockHeaders: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  },
  url: 'http://localhost:1026/v2/',
  headers: {
    'fiware-service': 'timeseries',
    'fiware-servicepath': '/',
    'Content-Type': 'application/json'
  }
};

const createKeyrockToken = async (name, password) => {
  console.log(name + ' ' + password);
  try {
    const response = await axios.post(
      config.keyrock + 'auth/tokens',
      {
        name: name,
        password: password
      },
      {
        headers: config.keyrockHeaders
      }
    );
    console.log(response);
    return response.data;
  } catch (err) {
    throw new Error(err);
  }
};

const getAllData = async () => {
  try {
    const response = await axios.get(config.url + 'entities/', {
      headers: config.headers
    });
    console.log(response);
    return response.data;
  } catch (err) {
    throw new Error(err);
  }
};

const getParamsChar = function (url) {
  return url.indexOf('?') === -1 ? '?' : '&';
};

const getEntity = async entity => {
  try {
    const response = await axios.get(
      config.url +
        'entities/' +
        entity +
        getParamsChar(entity) +
        'options=keyValues',
      {
        headers: config.headers
      }
    );
    return response;
  } catch (err) {
    throw new Error(err);
  }
};

const updateAttribute = async (entity, attrName, value) => {
  try {
    const response = await axios.put(
      config.url + 'entities/' + entity + '/attrs/' + attrName,
      { value: value },
      {
        headers: config.headers
      }
    );
    return response;
  } catch (err) {
    throw new Error(err);
  }
};

export default {
  createKeyrockToken,
  getAllData,
  getEntity,
  updateAttribute
};
