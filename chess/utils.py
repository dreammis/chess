# coding=utf-8
from flask import jsonify


def normal_jsonify(data=None, err_code='', err_msg='', status_code=200):
    return jsonify({'data': data, 'err_msg': err_msg, 'err_code': err_code}), status_code


def Error_jsonify(data=None, err_code=10010, err_msg='参数校验错误，详细参考data数据', status_code=200):
    return jsonify({'data': data, 'err_msg': err_msg, 'err_code': err_code}), status_code