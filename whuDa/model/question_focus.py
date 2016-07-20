# -*- coding: utf-8 -*-
from whuDa import db
import whuDa.model.users as db_users
class Question_focus(db.Model):
    __tablename__ = 'question_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    current_answer_count = db.Column(db.Integer, nullable=False)

    # 添加关注的问题
    def add_focus_question(self, uid, question_id, cnt):
        row = Question_focus(uid=uid, question_id=question_id, current_answer_count=cnt)
        if db.session.query(Question_focus).filter(Question_focus.uid == uid, Question_focus.question_id == question_id).first():
            return False
        db.session.add(row)
        db.session.commit()
        return True

    # 获取问题被关注的数量
    def get_question_foucs_count(self, question_id):
        return len(db.session.query(Question_focus).filter_by(question_id=question_id).all())

    # 判断用户是否已经关注该问题
    def question_focused(self, question_id, uid):
        return db.session.query(Question_focus).filter(Question_focus.uid == uid, Question_focus.question_id == question_id).first()

    # 获取一个用户关注的所有问题
    def get_user_focus_questions(self, username):
        return db.session.query(Question_focus).filter(Question_focus.uid == db_users.Users().get_uid_by_username(username))

    def get_user_focus_questions_by_uid(self, uid):
        return db.session.query(Question_focus).filter(
            Question_focus.uid == uid).all()

    # 获取用户关注的问题的数量
    def get_user_focus_question_count(self, username):
        return db.session.query(Question_focus).filter(Question_focus.uid == db_users.Users().get_uid_by_username(username)).count()

    def get_focus_questions_by_uid_and_page(self, uid, page_num, page_size):
        focus_questions = self.get_user_focus_questions_by_uid(uid)
        total_count = len(focus_questions)
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        if total_count > start_index:
            if total_count > end_index:
                return focus_questions[start_index:end_index]
            return focus_questions[start_index:]
        return []

    # 获取用户关注的所有问题id
    def get_user_focus_question_ids(self, uid):
        question_ids = []
        for item in Question_focus.query.filter_by(uid=uid).all():
            question_ids.append(item.question_id)
        return question_ids

    # 取消关注某个问题
    def question_cancel_focus(self, question_id, uid):
        row = Question_focus.query.filter(Question_focus.question_id == question_id, Question_focus.uid == uid).first()
        db.session.delete(row)
        db.session.commit()