import axios from 'axios';

const config = {
  url: 'http://localhost:1026/v2/',
  headers: {
    'fiware-service': 'timeseries',
    'fiware-servicepath': '/'
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

const getParamsChar = function (entity) {
  return entity.indexOf('?') === -1 ? '?' : '&';
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

export default {
  getAllData,
  getEntity
};
