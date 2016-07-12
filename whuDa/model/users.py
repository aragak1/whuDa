# -*- coding: utf-8 -*-
from whuDa import db
from time import time
from hashlib import md5
salt = '3JJLohSJXbJUXYxp'


class Users(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.Integer, default=2)   # 0代表女，1代表男，2代表保密
    birthday = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    introduction = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    qq = db.Column(db.String(16))
    phone = db.Column(db.String(16))
    website = db.Column(db.String(255))
    view_count = db.Column(db.Integer, nullable=False, default=0)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    group_id = db.Column(db.Integer, nullable=False, default=2)  # 0为管理员，1为普通用户，2为待审核用户
    notification_unread = db.Column(db.Integer, nullable=False, default=0)
    message_unread = db.Column(db.Integer, nullable=False, default=0)
    invite_count = db.Column(db.Integer, nullable=False, default=0)
    question_count = db.Column(db.Integer, nullable=False, default=0)
    answer_count = db.Column(db.Integer, nullable=False, default=0)
    topic_focus_count = db.Column(db.Integer, nullable=False, default=0)
    reg_time = db.Column(db.Integer)
    last_login = db.Column(db.Integer)
    last_ip = db.Column(db.String(255))
    forbidden = db.Column(db.Integer, default=0)  # 1代表被禁止
    avatar_url = db.Column(db.String(255), default="static/img/avatar/avatar.png")

    # 注册
    def register(self, username, password, email, last_ip):
        user = Users(username=username,
                     password=md5(password + salt).hexdigest(),
                     email=email,
                     reg_time=time(),
                     last_ip=last_ip,
                     last_login=time())
        if db.session.query(Users).filter(Users.username == username).first() or \
                db.session.query(Users).filter(Users.username == username).first():
            return False
        else:
            db.session.add(user)
            db.session.commit()
            return True

    # 登录验证
    def vaild(self, username, password, login_type):
        if login_type == 'email':
            user = db.session.query(Users).filter(Users.email == username).first()
        elif login_type == 'username':
            user = db.session.query(Users).filter(Users.username == username).first()
        if user:
            if md5(password + salt).hexdigest() == user.password:
                return True
            else:
                return False
        return False

    # 获通过用户名取一个user
    def get_user(self, username):
        return db.session.query(Users).filter(Users.username == username).first()