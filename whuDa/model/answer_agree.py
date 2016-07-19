# -*- coding: utf-8 -*-
from whuDa import db
'''id int(11) unsigned not null auto_increment comment '自增主键',
    question_id int(11) not null comment '赞同问题的ID',
    answer_id int(11) not null comment '被赞回答的ID',
    agree_uid int(11) not null comment '被赞用户的UID',
    uid int(11) not null comment '赞同用户的UID',
	uid = db.Column(db.Integer, primary_key=True)
'''
class Anser_agree:
	id=db.Column(db.Integer,primary_key=True);
	question_id=db.Column(db.Integer,nullable=False);
	answer_id=db.Column(db.Integer,nullable=False);
	agree_uid=db.Column(db.Integer,nullable=False);
	uid = db.Column(db.Integer, nullable=False);