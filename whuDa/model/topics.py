# -*- coding: utf-8 -*-
from whuDa import db
from sqlalchemy import desc
import whuDa.model.topic_focus as db_topic_focus
import whuDa.model.topic_question as db_topic_question
from math import ceil


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
        return Topics.query.filter_by(topic_id=topic_id).first().name

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

    # 按照页数来获取所有的话题数据, 按照问题数+关注数的和排序
    def get_topics_by_page(self, page_num, page_size):
        total_count = Topics.query.count()
        start_index = (page_num-1)*page_size
        end_index = start_index + page_size
        datas = []
        if total_count > start_index:
            for topic in Topics.query.all():
                temp_dict = {
                    'topic_id': topic.topic_id,
                    'topic_focus': db_topic_focus.Topic_focus().get_foucs_count(topic.topic_id),
                    'topic_question_count': db_topic_question.Topic_question().get_question_count(topic.topic_id),
                    'topic_name': self.get_topic_name_by_id(topic.topic_id),
                    'topic_url': self.get_topic_url(topic.topic_id),
                    'last_week_question_count': db_topic_question.Topic_question().get_last_week_question_count(topic.topic_id),
                    'last_month_question_count': db_topic_question.Topic_question().get_last_month_question_count(topic.topic_id)
                }
                datas.append(temp_dict)
                datas.sort(cmp=lambda a, b: int(b['topic_question_count'] + b['topic_focus'] - a['topic_question_count'] - a['topic_focus']))
            if total_count > end_index:
                return datas[start_index:end_index]
            return datas[start_index:]
        return datas

    # 获取所有的话题数目
    def get_topic_count(self):
        return Topics.query.count()

    # 获取最大的话题id
    def get_max_topic_id(self):
        return Topics.query.order_by(desc(Topics.topic_id)).first().topic_id

    # 测试一个number是否为topic_id
    def is_topic_id(self, number):
        return Topics.query.filter_by(topic_id=number).first()

    # 根据id获取话题
    def get_topic_by_id(self, topic_id):
        return Topics.query.filter_by(topic_id=topic_id).first()
