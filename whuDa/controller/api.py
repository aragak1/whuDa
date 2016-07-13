# _*_ coding:utf8 _*_
from whuDa import app
import whuDa.model.topics as db_topics
import json


# 根据关键字返回匹配的话题
@app.route('/api/topic/like/<keyword>.json')
def get_topics_by_keyword(keyword):
    topics = db_topics.Topics().get_by_keyword(keyword)
    data = []
    for topic in topics:
        temp_dict = {
            'topic_id': topic.topic_id,
            'name': topic.name,
            'introduction': topic.introducation,
            'topic_url': topic.topic_url
        }
        data.append(temp_dict)
    return json.dumps(data, ensure_ascii=False)


# 根据话题名称返回精确的话题
@app.route('/api/topic/<name>.json')
def get_topic_by_name(name):
    topic = db_topics.Topics().get_by_name(name)
    data = {
        'topic_id': topic.topic_id,
        'name': topic.name,
        'introduction': topic.introducation,
        'topic_url': topic.topic_url
    }
    return json.dumps(data, ensure_ascii=False)