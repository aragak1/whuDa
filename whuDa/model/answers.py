# _*_ coding:utf8 _*_
from whuDa import db
from time import time
from sqlalchemy import desc
import whuDa.model.questions as db_questions
import whuDa.model.users as db_users


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

    # 判断用户是否已经回复某一个问题
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
        return db.session.query(Answers).filter_by(question_id=question_id).order_by(desc(Answers.agree_count)).all()

    # 获取问题的回复数
    def get_answer_count(self, question_id):
        return db.session.query(Answers).filter_by(question_id=question_id).count()

    # 获取最新的回答用户uid
    def get_last_answer_uid(self, question_id):
        return Answers.query.filter_by(question_id=question_id).first().answer_uid

    # 获取问题最新的回答
    def get_last_answer(self, question_id):
        return db.session.query(Answers).filter_by(question_id=question_id).order_by(desc(Answers.answer_time)).first()

    # 判断一个问题是否有回答
    def question_is_answered(self, question_id):
        if Answers.query.filter_by(question_id=question_id).count():
            return True
        return False

    # 获取一个用户的所有回答和回答对应的问题
    def get_user_answers_with_question(self, username):
        return db.session.query(Answers).filter(Answers.answer_uid == db_users.Users().get_uid_by_username(username))

    # 获取一个用户的所有回复并且按照时间由新到旧排序
    def get_user_answers_order_by_time(self, username):
        return db.session.query(Answers).filter(Answers.answer_uid == db_users.Users().get_uid_by_username(username)).\
            order_by(desc(Answers.answer_time)).all()

