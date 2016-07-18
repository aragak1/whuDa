# -*- coding: utf-8 -*-
from whuDa import db

class Anser_agree(db.Model):
    __tablename__ = 'answer_agree'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    answer_id = db.Column(db.Integer, nullable=False)
    agree_uid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)

    # 获取某个答案的赞同数
    def get_question_agree_count(self, question_id):
        return Anser_agree.query.filter_by(question_id=question_id).count()