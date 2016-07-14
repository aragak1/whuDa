# -*- coding: utf-8 -*-
from whuDa import db


class Topic_question(db.Model):
    __tablename__ = 'topic_question'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)

    # 添加问题所属的话题
    def add_to_topic(self, question_id, topic_id):
        if db.session.query(Topic_question).filter(question_id == question_id, topic_id == topic_id).first():
            return False
        row = Topic_question(topic_id=topic_id, question_id=question_id)
        db.session.add(row)
        db.session.commit()
        return True
