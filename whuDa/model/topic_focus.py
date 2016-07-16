# -*- coding: utf-8 -*-
from whuDa import db


class Topic_focus(db.Model):
    __tablename__ = 'topic_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)

    # 获取话题的关注数
    def get_foucs_count(self, topic_id):
        return db.session.query(Topic_focus).filter_by(topic_id=topic_id).count()

    # 获取用户关注的话题id
    def __get_user_foucs_topic_ids(self, uid):
        topic_ids = []
        for row in Topic_focus.query.filter_by(uid=uid).all():
            topic_ids.append(row.topic_id)
        return topic_ids

    # 获取用户关注的话题id和话题名
    def get_user_focus_topics(self, uid):
        import whuDa.model.topics as db_topics
        topic_ids = self.__get_user_foucs_topic_ids(uid)
        datas = []
        for topic_id in topic_ids:
            data = {
                'topic_id': topic_id,
                'topic_name': db_topics.Topics().get_topic_name_by_id(topic_id)
            }
            datas.append(data)
        return datas

    # 获取关注某个话题的用户
    def get_focus_uid(self, topic_id):
        uids = []
        for i in Topic_focus.query.filter_by(topic_id=topic_id).all():
            uids.append(i.uid)
        return uids
