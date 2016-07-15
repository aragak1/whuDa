# _*_ coding: utf-8 _*_
from whuDa import db


class Topic_question(db.Model):
    __tablename__ = 'topic_question'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)

    # 添加问题所属的话题
    def add_to_topic(self, question_id, topic_id):
        if db.session.query(Topic_question).filter(Topic_question.question_id == question_id, Topic_question.topic_id == topic_id).first():
            print '问题已属于该话题'
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


