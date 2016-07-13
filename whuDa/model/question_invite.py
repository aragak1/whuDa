# -*- coding: utf-8 -*-
from whuDa import db
'''question_invite_id int(11) unsigned not null auto_increment comment '邀请ID',
    question_id int(11) not null comment '邀请回答的问题ID',
    sender_uid int(11) not null comment '发送邀请的用户UID',
    recipient_uid int(11) not null comment '被邀请的用户UID',
    send_time int(10) not null comment '邀请发送时间',
    primary key(question_invite_id)'''
class Question_invite:
	question_invite_id=db.Column(db.Integer, primary_key=True);
	question_id=db.Column(db.Integer,nullable=False);
	sender_uid=db.Column(db.Integer,nullable=False);
	recipient_uid=db.Column(db.Integer,nullable=False);
	send_time=db.Column(db.Integer,nullable=False);