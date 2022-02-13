from flask import Flask, jsonify, make_response
import numpy as np
import boto3
import os
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


@app.route("/s3_upload")
def upload_to_s3():
    try:
        temp_file = open(file='/tmp/temp.upload', mode='w')
        temp_file.write('test string from local dev')
        temp_file.close()
        s3_client = boto3.client('s3')
        s3_client.upload_file('/tmp/temp.upload', 'tree-epi-site-bucket', 'temp.upload')
        os.remove('/tmp/temp.upload')
        return jsonify(message=f'Uploaded to s3!')
    except Exception as e:
        print(e)
        return make_response(jsonify(error=f'{e}'), 404)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found - homie!'), 404)
