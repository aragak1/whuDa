# -*- coding: utf-8 -*-
from whuDa import db

class Question_focus(db.Model):
    __tablename__ = 'question_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    current_answer_count = db.Column(db.Integer, nullable=False)

    # 添加关注的问题
    def add_focus_question(self, uid, question_id, cnt):
        row = Question_focus(uid=uid, question_id=question_id, current_answer_count=cnt)
        if db.session.query(Question_focus).filter(uid == uid, question_id == question_id).first():
            return False
        db.session.add(row)
        db.session.commit()
        return True

    # 获取问题被关注的数量
    def get_question_foucs_count(self, question_id):
        return len(db.session.query(Question_focus).filter_by(question_id=question_id).all())
