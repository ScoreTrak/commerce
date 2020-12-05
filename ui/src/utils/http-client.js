import store from '@/store';

function getCsrfToken() {
  const cookies = Object.fromEntries(
    document.cookie.split(';').map((cookie) => cookie.trim().split('=')),
  );
  return cookies.csrftoken;
}

function internalFetch(method, url, data) {
  return fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify(data),
  }).then((response) => {
    // Detect if the user is not logged in.
    // TODO: 403 as well?
    if (response.status === 401) {
      store.commit('setCurrentUser', null);
    }
    return response;
  });
}

export default class HttpClient {
  static delete(url, data) {
    return internalFetch('DELETE', url, data);
  }

  static get(url, data) {
    return internalFetch('GET', url, data);
  }

  static patch(url, data) {
    return internalFetch('PATCH', url, data);
  }

  static post(url, data) {
    return internalFetch('POST', url, data);
  }
}
