from flask import Flask, request, Response
import json
from utils import generate_api_key
import random
import threading
from apiGenHandler import apiGenHandler

lock = threading.Lock()
handler = apiGenHandler()

app = Flask(__name__)


@app.route('/')
def welcome():
    resp = {}
    resp["message"] = "API Key Generator Assignment from Codeuino for LF Mentorship"
    return Response(response=json.dumps(resp), status=200)


@app.route('/key', methods=['GET', 'POST'])
def apikey():
    """API route to generate keys for POST request and provide 
    avaliable keys for GET request

    Time Complexity:
        POST: O(lgn)
        GET: O(lgn)
    """
    if request.method == 'POST':
        stat = handler.gen_api_key()
        resp = {}
        code = 200
        resp["message"] = "Generated"
        if stat == False:
            resp["message"] = "Failed"
            code = 404
        return Response(response=json.dumps(resp), status=code)

    if request.method == 'GET':
        with lock:
            key = handler.get_available_api_key()
        resp = {}
        code = 200
        resp["message"] = "Success"
        resp["key"] = key
        if key is None:
            resp["message"] = "Failed"
            code = 404
        return Response(response=json.dumps(resp), status=code)


@app.route('/key/del/<apikey>', methods=['DELETE'])
def delete_apikey(apikey):
    """API route to delete the given keys

    Time Complexity:
        DELETE: O(lgn)
    """
    if request.method == 'DELETE':
        with lock:
            stat = handler.delete_api_key(apikey)
        resp = {}
        code = 200
        resp["message"] = "Success"
        if stat is None:
            resp["message"] = "Failed"
            code = 404
        return Response(response=json.dumps(resp), status=code)


@app.route('/key/unblock/<key>', methods=['POST'])
def apikey_unblock(key):
    """API route to unblock the given API key
    Time Complexity:
        POST: O(lgn)
    """
    stat = handler.unblock_api_key(key)
    resp = {}
    code = 200
    resp["message"] = "Success"
    if stat is None:
        resp["message"] = "Failed"
        code = 404
    return Response(response=json.dumps(resp), status=code)


@app.route('/key/poll/<key>', methods=['POST'])
def apikey_poll(key):
    """API route to poll for extending the API key expiry
    Time Complexity:
        POST: O(lgn)
    """
    stat = handler.poll_api_key(key)
    resp = {}
    code = 200
    resp["message"] = "Success"
    if stat is None:
        resp["message"] = "Failed"
        code = 404
    return Response(response=json.dumps(resp), status=code)

if __name__ == '__main__':
    app.run(threaded=True)