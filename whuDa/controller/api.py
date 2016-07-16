# _*_ coding:utf8 _*_
from whuDa import app
from utils import timestamp_datetime, get_user_url, get_dynamic_str
import whuDa.model.topics as db_topics
import whuDa.model.questions as db_questions
import whuDa.model.users as db_users
import whuDa.model.question_focus as db_question_focus
import whuDa.model.answers as db_answers
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


@app.route('/api/topic/<int:topic_id>/page/<int:page_num>', methods=['POST', 'GET'])
def get_topic_detail_questions_by_page(topic_id, page_num):
    questions = db_questions.Questions().get_questions_by_topic_id_and_page(topic_id=topic_id, page_num=page_num, page_size=15)
    datas = []
    for question in questions:
        data = {
            'question_id': question.question_id,
            'title': question.title,
            'username': db_users.Users().get_user_by_id(question.questioner_uid).username,
            'is_anonymous': question.is_anonymous,
            'question_focus_count': db_question_focus.Question_focus().get_question_foucs_count(question.question_id),
            'question_answer_count': db_answers.Answers().get_answer_count(question.question_id),
            'question_view_count': db_questions.Questions().get_question_view_count(question.question_id),
            'publish_time': timestamp_datetime(question.publish_time),
            'user_url': get_user_url(question.question_id),
            'dynamic_str': get_dynamic_str(question.question_id)
        }
        datas.append(data)
    return json.dumps(datas, ensure_ascii=False)