# -*- coding: utf-8 -*-
from whuDa import db
from time import time
from random import randint
import whuDa.model.topics as db_topics


class Topic_recommend(db.Model):
    __tablename__ = 'topic_recommend'

    id = db.Column(db.Integer, primary_key=True)
    recommend_time = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)

    # 获取今日推荐的topic_id
    def get_today_recommend_topic_id(self):
        return Topic_recommend.query.first().topic_id

    # 测试并修改今日推荐的topic_id
    def test_and_update_today_recommend_topic(self):
        if not Topic_recommend.query.count():
            item = Topic_recommend(recommend_time=time(), topic_id=1)
            db.session.add(item)
            db.session.commit()
        current_topic_id = Topic_recommend.query.first().topic_id

        # 距离上次修改是否已经过了一天
        if time() - Topic_recommend.query.first().recommend_time >= 86400:
            new_topic_id = randint(1, db_topics.Topics().get_max_topic_id())

            # 新的topic_id不能和上次相同且应该在topic_id中
            while new_topic_id == current_topic_id or not db_topics.Topics().is_topic_id(new_topic_id):
                new_topic_id = randint(1, db_topics.Topics().get_max_topic_id())

            # 修改为新的topic
            Topic_recommend.query.filter_by(new_topic_id=current_topic_id).\
                update({Topic_recommend.topic_id: new_topic_id, Topic_recommend.recommend_time: time()})
            db.session.commit()
        return True
