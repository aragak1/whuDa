# -*- coding: utf-8 -*-
from whuDa import db


class Topic_focus(db.Model):
    __tablename__ = 'topic_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)

    # 获取话题的关注数
    def get_foucs_count(self, topic_id):
        return db.session.query(Topic_focus).filter_by(topic_id=topic_id).count()