# -*- coding: utf-8 -*-
from whuDa import db


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
