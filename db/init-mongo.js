db = db.getSiblingDB('testing'); // switch to testing db

db.createUser({
  user: 'ytilsAdmin',
  pwd: 'ytilsPassword',
  roles: [{ role: 'readWrite', db: 'ytils' }]
});