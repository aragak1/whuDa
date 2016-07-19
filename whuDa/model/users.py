# -*- coding: utf-8 -*-
from whuDa import db
from time import time
from hashlib import md5
from sqlalchemy import desc
from random import shuffle
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
        if Users.query.filter_by(username=username).first() or \
                Users.query.filter_by(email=email).first():
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

    # 通过uid获取一个user
    def get_user_by_id(self, uid):
        return Users.query.filter_by(uid=uid).first()

    # 用户问题数加一
    def add_question_count(self, username):
        user = db.session.query(Users).filter(Users.username == username).first()
        if user:
            db.session.query(Users).filter(Users.username == username).update({
                Users.question_count: Users.question_count + 1})
            db.session.commit()
            return True
        return False

    # 用户回答数加一
    def add_answer_count(self, username):
        user = db.session.query(Users).filter_by(username=username).first()
        if user:
            db.session.query(Users).filter_by(username=username).update({
                Users.answer_count: Users.answer_count + 1})
            db.session.commit()
            return True
        return False

    # 根据用户名获取uid
    def get_uid_by_username(self, username):
        return db.session.query(Users.uid).filter(Users.username == username).first().uid

    # 根据uid获取用户名
    def get_username_by_uid(self, uid):
        user = Users.query.filter_by(uid=uid).first()
        return user.username

    # 获取前五个热门用户的数据(avatar_url, username, question_count, answer_count)
    def get_top5_users(self):
        datas = []
        users = Users.query.order_by(desc(Users.answer_count + Users.question_count + Users.view_count)).limit(5)
        for user in users:
            temp_dict = {
                'username': user.username,
                'avatar_url': user.avatar_url,
                'question_count': user.question_count,
                'answer_count': user.answer_count
            }
            datas.append(temp_dict)
        return datas

    # 获取前五个热门用户的数据(avatar_url, username, question_count, answer_count)
    def get_top3_users(self):
        datas = []
        users = Users.query.order_by(desc(Users.answer_count + Users.question_count + Users.view_count)).limit(3)
        for user in users:
            temp_dict = {
                'username': user.username,
                'avatar_url': user.avatar_url,
                'question_count': user.question_count,
                'answer_count': user.answer_count,
                'introduction': user.introduction
            }
            datas.append(temp_dict)
        shuffle(datas)
        return datas

    # 获取一个user的年月日的dict
    def get_birthday_dict(self, uid):
        from whuDa.controller.utils import get_date
        birthday =  Users.query.filter_by(uid=uid).first().birthday
        if not birthday:
            return get_date(0)
        return get_date(Users.query.filter_by(uid=uid).first().birthday)

    # 更新用户头像url
    def update_avatar_url(self, username, avatar_url):
        Users.query.filter_by(username=username).update({Users.avatar_url: avatar_url})
        db.session.commit()
        return True

    # 修改用户的个人信息
    def update_user_profile(self, username, sex, birthday, department_id, introduction, qq, mobile, website):
        user = Users.query.filter_by(username=username)
        user.update({Users.sex: sex,
                     Users.birthday: birthday,
                     Users.introduction: introduction,
                     Users.qq: qq,
                     Users.phone: mobile,
                     Users.department_id: department_id,
                     Users.website: website})
        db.session.commit()
        return True

    # 判断是否为当前用户密码
    def is_user_password(self, username, password):
        user = Users.query.filter_by(username=username).first()
        if md5(password + salt).hexdigest() == user.password:
            return True
        return False

    # 获取所有用户
    def get_all_users(self):
        return db.session.query(Users).all()

    # 获取用户的个数
    def get_users_count(self):
        return db.session.query(Users).count()

    # 查询用户名是否在数据库中
    def is_exist_username(self, username):
        if Users.query.filter_by(username=username).count():
            return True
        return False

