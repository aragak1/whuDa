# -*- coding: utf-8 -*-
from whuDa import db
'''question_favorite_id int(11) unsigned not null auto_increment comment '收藏的ID',
    uid int(11) not null comment '收藏问题的用户UID',
    question_id int(11) not null comment '收藏的问题ID',
    add_time int(10) not null comment '收藏时间',
    primary key (question_favorite_id)'''
class Question_favorite(db.Model):
	__tablename__ = 'question_favorite'

	question_favorite_id=db.Column(db.Integer, primary_key=True);
	uid=db.Column(db.Integer,nullable=False);
	question_id=db.Column(db.Integer,nullable=False);
	add_time=db.Column(db.Integer,nullable=False);


	def add_favorite(self, uid, question_id, add_time):
		favor = Question_favorite(uid=uid, question_id=question_id, add_time=add_time)
		db.session.add(favor)
		db.session.flush()
		db.session.commit()