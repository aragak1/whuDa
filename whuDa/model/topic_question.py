# _*_ coding: utf-8 _*_
from whuDa import db
import whuDa.model.questions as db_questions


class Topic_question(db.Model):
    __tablename__ = 'topic_question'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)

    # 添加问题所属的话题
    def add_to_topic(self, question_id, topic_id):
        if Topic_question.query.filter(Topic_question.question_id == question_id, Topic_question.topic_id == topic_id).first():
            return False
        row = Topic_question(topic_id=topic_id, question_id=question_id)
        db.session.add(row)
        db.session.commit()
        return True

    # 通过id获取问题所属的话题
    def get_topics_by_id(self, question_id):
        topic_ids = []
        topic_qustions =  db.session.query(Topic_question).filter_by(question_id=question_id).all()
        for topic_question in topic_qustions:
            topic_ids.append(topic_question.topic_id)
        return topic_ids

    # 获取话题下的问题数目
    def get_question_count(self, topic_id):
        return db.session.query(Topic_question).filter_by(topic_id=topic_id).count()

    # 一个话题下一周内发布的问题数
    def get_last_week_question_count(self, topic_id):
        count = 0
        for question in Topic_question.query.filter_by(topic_id=topic_id).all():
            if db_questions.Questions().is_published_in_this_week(question.question_id):
                count += 1
        return count

    # 一个话题下一个月内发布的问题数
    def get_last_month_question_count(self, topic_id):
        count = 0
        for question in Topic_question.query.filter_by(topic_id=topic_id).all():
            if db_questions.Questions().is_published_in_this_month(question.question_id):
                count += 1
        return count


