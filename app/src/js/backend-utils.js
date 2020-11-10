import axios from 'axios';
import store from '../store';

const config = {
  urlKeyrock: 'http://localhost:3005/',
  url: 'http://localhost:1027/v2/',
  headers: {
    'fiware-service': 'timeseries',
    'fiware-servicepath': '/',
    'Content-Type': 'application/json'
  }
};

const createKeyrockToken = async (name, password) => {
  try {
    const response = await axios.post(
      config.urlKeyrock + 'v1/auth/tokens',
      {
        name: name,
        password: password
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json'
        }
      }
    );
    return response;
  } catch (err) {
    throw new Error(err);
  }
};

const getKeyrockUser = async token => {
  try {
    const response = await axios.get(config.urlKeyrock + 'v1/auth/tokens', {
      headers: {
        'X-Auth-token': token,
        'X-Subject-token': token
      }
    });
    return response;
  } catch (err) {
    throw new Error(err);
  }
};

const createKeyrockAccessToken = async (name, password) => {
  try {
    const params = new URLSearchParams();
    params.append('username', name);
    params.append('password', password);
    params.append('grant_type', 'password');
    const response = await axios.post(
      config.urlKeyrock + 'oauth2/token',
      /* {
        username: name,
        password: password,
        grant_type: 'password'
      }, */
      params,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Accept: 'application/json'
        },
        auth: {
          username: 'tutorial-dckr-site-0000-xpresswebapp',
          password: 'tutorial-dckr-site-0000-clientsecret'
        }
      }
    );
    return response;
  } catch (err) {
    throw new Error(err);
  }
};

const setAxiosAuthToken = token => {
  // axios.defaults.headers.common.Authorization = token;
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
  // console.log(store.getters['user/getAuth'].access.access_token);
  const headers = config.headers;
  // headers['X-Auth-Token'] = 'Bearer ' + store.getters['user/getAuth'].token;
  headers.Authorization =
    'Bearer ' + store.getters['user/getAuth'].access.access_token;
  // console.log(headers);
  try {
    const response = await axios.get(
      config.url +
        'entities/' +
        entity +
        getParamsChar(entity) +
        'options=keyValues',
      {
        headers: headers
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
  setAxiosAuthToken,
  getKeyrockUser,
  createKeyrockAccessToken,
  getAllData,
  getEntity,
  updateAttribute
};
