# -*- coding: utf-8 -*-
from whuDa import db
from random import choice


class Topic_focus(db.Model):
    __tablename__ = 'topic_focus'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)

    # 用户关注话题
    def add_focus_topic(self, uid, topic_id):
        row = Topic_focus(uid=uid, topic_id=topic_id)
        if self.user_focus_topic(uid,topic_id):
            return False
        db.session.add(row)
        db.session.commit()
        return True
    # 用户取消关注话题
    def cancel_focus_topic(self, uid,topic_id):
        print topic_id
        row = Topic_focus.query.filter(Topic_focus.topic_id == topic_id, Topic_focus.uid == uid).first()
        print row
        db.session.delete(row)
        db.session.commit()
    #判断用户是否已经关注该话题
    def user_focus_topic(self,uid,topic_id):
        if db.session.query(Topic_focus).filter(Topic_focus.uid == uid, Topic_focus.topic_id == topic_id).first():
            return True
        else:
            return False
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

    # 获取一个用户关注的所有话题
    def get_user_focus_topics(self, uid):
        import whuDa.model.topic_question as db_topic_question
        import whuDa.model.topics as db_topics
        focus_topics = db.session.query(Topic_focus).filter(Topic_focus.uid == uid).all()
        focus_topics_datas = []
        for focus_topic in focus_topics:
            data = {
                'topic_id': focus_topic.topic_id,
                'topic_focus': self.get_foucs_count(focus_topic.topic_id),
                'topic_question_count': db_topic_question.Topic_question().get_question_count(focus_topic.topic_id),
                'topic_name': db_topics.Topics().get_topic_name_by_id(focus_topic.topic_id),
                'topic_url': db_topics.Topics().get_topic_url(focus_topic.topic_id),
                'last_week_question_count': db_topic_question.Topic_question().get_last_week_question_count(focus_topic.topic_id),
                'last_month_question_count': db_topic_question.Topic_question().get_last_month_question_count(focus_topic.topic_id)
            }
            focus_topics_datas.append(data)
        return focus_topics_datas

    # 按照分页获取一个用户关注的所有话题
    def get_user_focus_topics_by_page(self, uid, page_num, page_size):
        focus_topics = self.get_user_focus_topics(uid)
        total_count = len(focus_topics)
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        if total_count > start_index:
            if total_count > end_index:
                return focus_topics[start_index:end_index]
            return focus_topics[start_index:]
        return []

