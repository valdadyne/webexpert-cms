from app.controllers import app

app.config['MONGO_DBNAME'] = "webexpert-cms"
app.config['MONGO_URI'] = "mongodb://webexpert-admin:dropzone2016@ds059496.mlab.com:59496/webexpert-cms"

app.secret_key = "my-secret"