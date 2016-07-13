# _*_ coding:utf8 _*_
from whuDa import app
import whuDa.model.topics as db_topics
import json


@app.route('/topic/<keyword>.json')
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