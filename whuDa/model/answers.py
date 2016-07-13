# -*- coding: utf-8 -*-
from whuDa import db
'''answer_id int(11) unsigned not null auto_increment comment '回答ID',
    question_id int(11) not null comment '所回答问题的ID',
    answer_uid int(11) not null comment '回答用户的UID',
    content text not null comment '回答内容',
    is_anonymous tinyint(1) not null default 0 comment '是否匿名',
    answer_time int(10) not null comment '回答时间',
    agree_count int(10) not null default 0 comment '赞同数',
    disagree_count int(10) not null default 0 comment '反对数',
	uid = db.Column(db.Integer, primary_key=True)'''
class Answers:
	answer_id=db.Column(db.Integer, primary_key=True);
	question_id=db.Column(db.Integer, nullable=False);
	answer_uid=db.Column(db.Integer, nullable=False);
	content=db.Column(db.Text,nullable=False);
	is_anonymous=db.Column(db.Integer, nullable=False,default=0);
	answer_time=db.Column(db.Integer, nullable=False);
	agree_count=db.Column(db.Integer, nullable=False,default=0);
	disagree_count=db.Column(db.Integer, nullable=False);
	