/*
** link.js
*/

const apiRoute = '/api/v1/';
const linksRoute = `${apiRoute}links/`;

function handleErrors(response) {
  if (!response.ok) {
    throw Error(`${response.status}, ${response.statusText}`);
  }
  return response;
}

function fetchApi(route, options) {
  return fetch(route, options)
    .then(handleErrors)
    .then(response => response.json())
    .catch(console.log);
}

class LinkRepository {
  constructor(route = linksRoute) {
    this._route = route;
  }

  get(key) {
    return fetchApi(this._route + key);
  }

  find(page = 1, size = 20) {
    return fetchApi(`${this._route}?page=${page}&size=${size}`);
  }

  save(link) {
    return fetchApi(this._route, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(link),
    });
  }
}

exports.LinkRepository = LinkRepository;
