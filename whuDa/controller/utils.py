# _*_ coding:utf8 _*_
from flask import session


def is_login():
    if 'username' in session:
        return True
    return False
