# -*- coding: utf-8 -*-
from whuDa import db

class Anser_agree(db.Model):
    __tablename__ = 'answer_agree'

    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, nullable=False)
    agree_uid = db.Column(db.Integer, nullable=False)

    # 获取某个答案的赞同数
    def get_answer_agree_count(self, answer_id):
        return Anser_agree.query.filter_by(answer_id=answer_id).count()

    # 判断用户是否已经赞了某个回答
    def agree(self, uid, answer_id):
        if Anser_agree.query.filter(Anser_agree.answer_id == answer_id, Anser_agree.agree_uid == uid).count():
            return True
        return False

    # 赞同某个答案
    def add_agree(self, uid, answer_id):
        row = Anser_agree(answer_id=answer_id, agree_uid=uid)
        db.session.add(row)
        db.session.commit()

    # 取消赞同某个答案
    def delete_agree(self, uid, answer_id):
        row = Anser_agree.query.filter(Anser_agree.answer_id == answer_id, Anser_agree.agree_uid == uid).first()
        db.session.delete(row)
        db.session.commit()
