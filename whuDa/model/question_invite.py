# -*- coding: utf-8 -*-
from whuDa import db


class Question_invite(db.Model):
    question_invite_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    sender_uid = db.Column(db.Integer, nullable=False)
    recipient_uid = db.Column(db.Integer, nullable=False)
    send_time = db.Column(db.Integer, nullable=False)
