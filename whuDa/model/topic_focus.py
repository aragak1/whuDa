# -*- coding: utf-8 -*-
from whuDa import db
from random import choice


class Topic_focus(db.Model):
    __tablename__ = 'topic_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)

    # 获取话题的关注数
    def get_foucs_count(self, topic_id):
        return db.session.query(Topic_focus).filter_by(topic_id=topic_id).count()

    # 获取用户关注的话题id
    def get_user_foucs_topic_ids(self, uid):
        topic_ids = []
        for row in Topic_focus.query.filter_by(uid=uid).all():
            topic_ids.append(row.topic_id)
        return topic_ids

    # 获取用户关注的话题id和话题名
    def get_user_focus_topics(self, uid):
        import whuDa.model.topics as db_topics
        topic_ids = self.get_user_foucs_topic_ids(uid)
        datas = []
        for topic_id in topic_ids:
            data = {
                'topic_id': topic_id,
                'name': db_topics.Topics().get_topic_name_by_id(topic_id)
            }
            datas.append(data)
        return datas

    # 获取关注某个话题的用户
    def get_focus_uid(self, topic_id):
        uids = []
        for i in Topic_focus.query.filter_by(topic_id=topic_id).all():
            uids.append(i.uid)
        return uids

    # 获取一个用户关注的话题下所有的问题id
    def get_question_ids_under_topic(self, uid):
        import whuDa.model.topic_question as db_topics_question
        topic_ids = self.get_user_foucs_topic_ids(uid)
        question_ids = []
        for topic_id in topic_ids:
            question_ids += db_topics_question.Topic_question().get_question_id_by_topic_id(topic_id)
        return question_ids

    # 获取一个关注了某个话题的用户的username
    def get_topic_focus_username(self, topic_id):
        import whuDa.model.users as db_users
        focus_uid = self.get_focus_uid(topic_id)
        if focus_uid:
            return db_users.Users().get_username_by_uid(choice(focus_uid))
        return []

