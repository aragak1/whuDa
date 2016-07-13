# -*- coding: utf-8 -*-
from whuDa import db
'''id int(11) unsigned not null auto_increment comment '自增主键',
    question_id int(11) not null comment '反对问题的ID',
    answer_id int(11) not null comment '被反对回答的ID',
    disagree_uid int(11) not null comment '被反对用户的UID',
    uid int(11) not null comment '反对用户UID',
	uid = db.Column(db.Integer, primary_key=True)'''
class Answer_disagree:
	id=db.Column(db.Integer,primary_key=True);
	question_id=db.Column(db.Integer,nullable=False);
	answer_id=db.Column(db.Integer,nullable=False);
	disagree_uid=db.Column(db.Integer,nullable=False);
	uid=db.Column(db.Integer,nullable=False);