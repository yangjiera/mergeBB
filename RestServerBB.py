#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function:
【记录】使用Python的IDE：Eclipse+PyDev
 
http://www.crifan.com/try_with_python_ide_eclipse_pydev
 
Author:     Crifan Li
Version:    2012-12-29
Contact:    admin at crifan dot com
"""
 
from flask import Flask, jsonify, abort, make_response, request
from restWrapper import *
from mergeBB import *
import json

app = Flask(__name__)


@app.route('/merge/api/v1.0/', methods = ['GET'])
def get_tasks():
    return jsonify( { 'introduction': 'this service merges bounding boxes identified by multiple workers' } )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/merge/api/v1.0/mergeBB', methods = ['POST'])
def merge():
    rjson = json.loads(json.dumps(request.json, ensure_ascii=False).encode('utf8'))
    BBs = []
    for rbb in rjson:
        BBs.append(rbb)
    inputname, bb_info = wrapBB(BBs)
    
    iname = mergeBB(inputname)
    
    rturnjson = wrapABB(iname, bb_info)
    print rturnjson
    return rturnjson, 201

@app.route('/')
def index():
    return "Merge Bounding Box service is available, please Post to /merge/api/v1.0/mergeBB\n"

if __name__ == '__main__':
    app.run(debug = True, host='145.100.58.60', port=12345)