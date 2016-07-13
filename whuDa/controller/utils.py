# _*_ coding:utf8 _*_
from flask import session
import re


def is_login():
    if 'username' in session:
        return True
    return False


def check_mail(email):
    if re.match('[a-zA-Z0-9_.-]*@[a-zA-Z0-9._-]', email, 0):
        return True
    return False


def check_username(username):
    if re.match('[a-zA-Z](.*)', username, 0):
        return True
    return False
