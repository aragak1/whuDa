# -*- coding: utf-8 -*-
from whuDa import db
from time import time


'''
    question_id int(11) unsigned not null auto_increment comment '问题ID',
    questioner_uid int(11) not null comment '提问者UID',
    title varchar(255) not null default '' comment '问题标题',
    content text not null comment '问题描述',
    publish_time int(10) not null comment '发布时间',
    update_time int(10) not null comment '最近修改时间',
    is_anonymous tinyint(1) not null default 0 comment '是否匿名',
    view_count int(10) not null default 0 comment '浏览次数',
    is_lock tinyint(1) not null default 0 comment '问题是否被锁定'
'''


class Questions(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    questioner_uid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)
    is_anonymous = db.Column(db.Integer, nullable=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, default=0)
    is_lock = db.Column(db.Integer, nullable=False, default=0)

    # 添加一个新问题
    def publish(self, questioner_uid, title, content, is_anonymous):
        question = Questions(
            questioner_uid=questioner_uid,
            title=title,
            content=content,
            publish_time=time(),
            update_time=time(),
            is_anonymous=is_anonymous)
        db.session.add(question)
        db.session.flush()
        question_id = question.question_id
        db.session.commit()
        return question_id

