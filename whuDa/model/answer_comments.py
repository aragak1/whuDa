# -*- coding: utf-8 -*-
from whuDa import db
'''id int(11) unsigned not null auto_increment comment '自增主键',
    answer_id int(11) not null comment '问题ID',
    content text not null comment '评论内容',
    uid int(11) not null comment '评论者UID',
    publish_time int(10) not null comment '评论时间',
	uid = db.Column(db.Integer, primary_key=True)
'''
class Answer_comments:
	id==db.Column(db.Integer,primary_key=True);
	answer_id=db.Column(db.Integer,nullable=False);
	content=db.Column(db.Text,nullable=False);
	uid=db.Column(db.Integer,nullable=False);
	publish_time=db.Column(db.Integer,nullable=False);