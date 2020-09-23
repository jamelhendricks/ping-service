from flask import Flask, jsonify
from requests.auth import HTTPDigestAuth
from flask_httpauth import HTTPDigestAuth
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()
users = {
    "vcu": "rams",
}
pong_url = 'https://pong-service-455.herokuapp.com/pong'

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/')
@auth.login_required
def index():
    username = auth.username()
    password = auth.get_password_callback(username)
    user = (jsonify({'username': username}),
            jsonify({'password': password}))
    return "{}".format(user)


@app.route('/ping')
@auth.login_required
def PingService():
    start = datetime.datetime.now()
    username = auth.username()
    password = auth.get_password_callback(username)

    pong_response = requests.get(
        pong_url, auth=requests.auth.HTTPDigestAuth(username, password))
    end = datetime.datetime.now()
    elapsed = end - start
    elapsed = elapsed.microseconds / 1000
    # elapsed = pong_response.elapsed.microseconds / 1000 <-- returns 0 for time, possibly interference w/ headers from auth
    kickback = {'pingpong_t': elapsed}
    return jsonify(kickback), 201
