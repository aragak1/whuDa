# -*- coding: utf-8 -*-
from whuDa import db
from sqlalchemy import desc
import whuDa.model.topic_focus as db_topic_focus
import whuDa.model.topic_question as db_topic_question


class Topics(db.Model):
    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    introducation = db.Column(db.Text)
    topic_url = db.Column(db.String(255), default='static/img/topic/topic.png')

    # 获取所有
    def get_all_topics(self):
        return db.session.query(Topics).all()

    # 根据关键字匹配
    def get_by_keyword(self, keyword):
        key_str = '{}{}{}'.format('%', keyword, '%')
        return db.session.query(Topics).filter(Topics.name.like(key_str))

    # 根据话题名精确匹配
    def get_by_name(self, topic_name):
        return db.session.query(Topics).filter(Topics.name == topic_name).first()

    # 根据话题名字获取话题id
    def get_topic_id_by_name(self, topic_name):
        topic = db.session.query(Topics, Topics.topic_id).filter(Topics.name == topic_name).first()
        return topic.topic_id

    # 根据话题id获取话题名字
    def get_topic_name_by_id(self, topic_id):
        return db.session.query(Topics).filter_by(topic_id=topic_id).first().name

    # 返回所有的话题id
    def get_all_topics_id(self):
        topic_ids = []
        topics = db.session.query(Topics).all()
        for topic in topics:
            topic_ids.append(topic.topic_id)
        return topic_ids

    # 获取话题url
    def get_topic_url(self, topic_id):
        return db.session.query(Topics).filter_by(topic_id=topic_id).first().topic_url

    # 获取前五个热门话题需要的数据(topic_id, topic_name, topic_url, 问题数， 关注人数)
    def get_top5_topics(self):
        datas = []
        # topic_id以及对应的关注
        topic_and_focus_count = []

        for topic_id in self.get_all_topics_id():
            temp_dict = {
                'topic_id': topic_id,
                'focus_count': db_topic_focus.Topic_focus().get_foucs_count(topic_id),
                'question_count': db_topic_question.Topic_question().get_question_count(topic_id)}
            topic_and_focus_count.append(temp_dict)

        topic_and_focus_count.sort(lambda a, b: int(b['focus_count']+b['question_count'] - a['focus_count']-a['question_count']))

        if len(topic_and_focus_count) > 5:
            topic_and_focus_count = topic_and_focus_count[0:5]

        for item in topic_and_focus_count:
            temp_dict = {
                'topic_id': item['topic_id'],
                'focus_count': item['focus_count'],
                'topic_name': self.get_topic_name_by_id(item['topic_id']),
                'question_count': item['question_count'],
                'topic_url': self.get_topic_url(item['topic_id'])
            }
            datas.append(temp_dict)
        return datas
