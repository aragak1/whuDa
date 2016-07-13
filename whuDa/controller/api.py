# _*_ coding:utf8 _*_
from whuDa import app
import whuDa.model.topics as db_topics
import json


# 根据关键字返回匹配的话题
@app.route('/api/topic/like/<keyword>.json')
def get_topics_by_keyword(keyword):
    topics = db_topics.Topics().get_by_keyword(keyword)
    topics_list = []
    data = {'topics': topics_list}
    for topic in topics:
        temp_dict = {
            'topic_id': topic.topic_id,
            'name': topic.name,
            'introduction': topic.introducation,
            'topic_url': topic.topic_url
        }
        data['topics'].append(temp_dict)
    return json.dumps(data, ensure_ascii=False)


# 判断是否找到匹配
@app.route('/api/topic/find/<keyword>.find', methods=['POST', 'GET'])
def keyword_find(keyword):
    if db_topics.Topics().get_by_keyword(keyword).first():
        return 'success'
    return 'failed'


# 根据话题名称返回精确的话题
@app.route('/api/topic/<name>.json', methods=['POST', 'GET'])
def get_topic_by_name(name):
    topic = db_topics.Topics().get_by_name(name)
    data = {
        'topic_id': topic.topic_id,
        'name': topic.name,
        'introduction': topic.introducation,
        'topic_url': topic.topic_url
    }
    return json.dumps(data, ensure_ascii=False)