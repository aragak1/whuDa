# -*- coding: utf-8 -*-
from whuDa import db
'''message_id int(11) unsigned not null auto_increment comment '私信ID',
    session_id int(11) not null comment '会话ID',
    sender_uid int(11) not null comment '发送者UID',
    recipient_uid int(11) not null comment '接受者UID',
    content text not null comment '私信内容',
    send_time int(10) not null comment '发送时间',
    is_read tinyint(1) not null default 0 comment '是否已读','''
class Message:
	message_id=db.Column(db.Integer, primary_key=True);
	session_id=db.Column(db.Integer,nullable=False);
	sender_uid=db.Column(db.Integer,nullable=False);
	recipient_uid=db.Column(db.Integer,nullable=False);
	content=db.Column(db.Text,nullable=False);
	send_time=db.Column(db.Integer,nullable=False);
	is_read=db.Column(db.Integer,nullable=False,default=0);
	