import re
from collections import Iterable
from functools import wraps

from app.utils.response import ResMsg
from flask import jsonify


def model_to_dict(result):
    # 转换完成后，删除  '_sa_instance_state' 特殊属性
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res
                   in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp

    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')


def route(bp, *args, **kwargs):
    """
    路由设置, 统一返回格式
    :param bp: 蓝图
    :return:
    """
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            rv = f(*args, **kwargs)
            # 响应函数返回整数和浮点型
            if isinstance(rv, (int, float)):
                res = ResMsg()
                res.update(data=rv)
                return jsonify(res.data)
            # 响应函数返回元组
            elif isinstance(rv, tuple):
                # 判断是否为多个参数
                if len(rv) >= 3:
                    return jsonify(rv[0]), rv[1], rv[2]
                else:
                    return jsonify(rv[0]), rv[1]
            # 响应函数返回字典
            elif isinstance(rv, dict):
                return jsonify(rv)
            # 响应函数返回字节
            elif isinstance(rv, bytes):
                rv = rv.decode('utf-8')
                return jsonify(rv)
            else:
                return jsonify(rv)

        return wrapper

    return decorator


def view_route(f):
    def decorator(*args, **kwargs):
        rv = f(*args, **kwargs)
        if isinstance(rv, (int, float)):
            res = ResMsg()
            res.update(data=rv)
            return jsonify(res.data)
        elif isinstance(rv, tuple):
            if len(rv) >= 3:
                return jsonify(rv[0]), rv[1], rv[2]
            else:
                return jsonify(rv[0]), rv[1]
        elif isinstance(rv, dict):
            return jsonify(rv)
        elif isinstance(rv, bytes):
            rv = rv.decode('utf-8')
            return jsonify(rv)
        else:
            return jsonify(rv)

    return decorator


class EmailTool(object):
    @staticmethod
    def check_email(email):
        v_email = re.match((r"^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@"
                            "([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"),
                           email)
        if v_email is None or v_email.group() is None:
            return False
        else:
            return True


class PhoneTool(object):
    """
    手机号码验证工具
    """

    @staticmethod
    def check_phone(phone):
        """
        验证手机号是否为中国手机号码
        :param phone:手机号码
        :return:
        """
        if len(str(phone)) == 11:
            v_phone = re.match(r'^1[3-9][0-9]{9}$', phone)
            if v_phone:
                return True
        return False