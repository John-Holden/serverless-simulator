from flask import Flask, jsonify, make_response
import numpy as np

app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root - homie!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path - homie!')


@app.route("/numpy_test")
def numpy_test():
    return jsonify(message=f'Hello from numpy_test. array {np.array([1])}!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found - homie!'), 404)
