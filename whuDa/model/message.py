# -*- coding: utf-8 -*-
from whuDa import db
from whuDa.controller.utils import timestamp_datetime
import whuDa.model.users as db_users


class Message(db.Model):
    __tablename__ = 'message'

    message_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False)
    sender_uid = db.Column(db.Integer, nullable=False)
    recipient_uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    send_time = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Integer, nullable=False, default=0)

    # 获取用户的所有私信会话
    def get_user_session_ids(self, uid):
        session_ids = []
        for message in Message.query.filter_by(recipient_uid=uid).all():
            if message.session_id not in session_ids:
                session_ids.append(message.session_id)
        return session_ids

    # 获取一次会话中最早的一次消息
    def get_first_session_message(self, session_id, uid):
        return Message.query.filter(Message.recipient_uid == uid, Message.session_id == session_id).order_by(Message.send_time).first()

    # 获取一次会话中的消息条数
    def get_session_message_count(self, session_id):
        return Message.query.filter_by(session_id=session_id).count()

    # 获取用户的私信数据(sender_uid, sender_avatar_url, content, message_count)
    def get_messages(self, uid):
        datas = []
        session_ids = self.get_user_session_ids(uid)
        for session_id in session_ids:
            first_message = self.get_first_session_message(session_id, uid)
            sender = db_users.Users().get_user_by_id(first_message.sender_uid)
            data = {
                'session_id': session_id,
                'content': first_message.content,
                'sender_avatar': sender.avatar_url,
                'sender_name': sender.username,
                'send_time': timestamp_datetime(first_message.send_time),
                'message_count': self.get_session_message_count(session_id)
            }
            datas.append(data)
        return datas