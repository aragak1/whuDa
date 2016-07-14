# _*_ coding:utf8 _*_
from whuDa import db
from time import time


class Answers(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    answer_uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Integer, nullable=False)
    answer_time = db.Column(db.Integer, nullable=False)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    # 判断用户是否已经回复
    def answered(self, uid, question_id):
        if db.session.query(Answers).filter(Answers.answer_uid == uid, Answers.question_id == question_id).first():
            return True
        return False

    # 添加一条回复
    def add_answer(self, question_id, answer_uid, content, is_anonymous):
        answer = Answers(question_id=question_id,
                         answer_uid=answer_uid,
                         content=content,
                         is_anonymous=is_anonymous,
                         answer_time=time())
        db.session.add(answer)
        db.session.flush()
        answer_id = answer.answer_id
        db.session.commit()
        return answer_id

    # 获取所有的回复，按照票数排序
    def get_all_answer(self, question_id):
        return db.session.query(Answers).filter_by(question_id=question_id).order_by(Answers.agree_count).all()
