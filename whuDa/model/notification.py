# -*- coding: utf-8 -*-
from whuDa import db
'''notification_id int(11) unsigned not null auto_increment comment '通知ID',
    sender_uid int(11) not null comment '发送者UID',
    recipient_uid int(11) not null comment '接受者UID',
    content text not null comment '通知内容',
    send_time int(10) not null comment '发送时间',
    is_read tinyint(1) not null default 0 comment '是否已读'
'''


class Notification(db.Model):
	__tablename__ = 'notification'
	notification_id=db.Column(db.Integer, primary_key=True);
	sender_uid=db.Column(db.Integer,nullable=False);
	recipient_uid=db.Column(db.Integer,nullable=False);
	content=db.Column(db.Text,nullable=False);
	send_time=db.Column(db.Integer,nullable=False);
	is_read=db.Column(db.Integer,nullable=False,default=0);
	#通过接受者id获取一个notification
	def get_notification_by_ruid(self,recipient_uid):
		return db.session.query(Notification).filter(Notification.recipient_uid == recipient_uid)
	#将一个通知变为已读
	def has_read(self,notification_id):
		notification=Notification.query.filter_by(notification_id=notification_id).first()
		if notification.is_read==0:
			db.session.query(Notification).filter(Notification.notification_id == notification_id).update({Notification.is_read: 1})
			db.session.commit()
			return "标记为未读"
		else:
			db.session.query(Notification).filter(Notification.notification_id == notification_id).update({Notification.is_read: 0})
			db.session.commit()
			return "标记为已读"
	#将所有通知变为已读
	def read_all(self):
		print 'read all'
		db.session.query(Notification).update({Notification.is_read: 1})
		db.session.commit()
		return
	#删除一个通知
	def delete(self,notification_id):
		db.session.query(Notification).filter(Notification.notification_id == notification_id).delete()
		db.session.commit()