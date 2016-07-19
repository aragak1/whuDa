# _*_ coding:utf8 _*_
from whuDa import app
from utils import timestamp_datetime, get_user_url, get_dynamic_str
import whuDa.model.topics as db_topics
import whuDa.model.questions as db_questions
import whuDa.model.users as db_users
import whuDa.model.question_focus as db_question_focus
import whuDa.model.answers as db_answers
import json
from utils import get_past_time, get_dynamic_datas_by_page


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


@app.route('/api/topic/<int:topic_id>/page/<int:page_num>.json', methods=['POST', 'GET'])
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
            'dynamic_str': get_dynamic_str(question.question_id),
            'avatar_url': db_users.Users().get_user_by_id(question.questioner_uid).avatar_url
        }
        datas.append(data)
    return json.dumps(datas, ensure_ascii=False)


@app.route('/api/user_question/<int:uid>/page/<int:page_num>.json', methods=['POST', 'GET'])
def get_user_question_by_page(uid, page_num):
    questions = db_questions.Questions().get_questions_by_username_and_page(uid=uid, page_num=page_num, page_size=15)
    datas = []
    for question in questions:
        data = {
            'question_id': question.question_id,
            'title': question.title,
            'reply_count': db_questions.Questions().get_question_reply_count(question.question_id),
            'view_count': question.view_count,
            'focus_count': db_questions.Questions().get_question_focus_count(question_id=question.question_id),
            'publish_time': get_past_time(question.publish_time)
        }
        datas.append(data)
    return json.dumps(datas, ensure_ascii=False)


@app.route('/api/user_answer/<int:uid>/page/<int:page_num>.json', methods=['POST', 'GET'])
def get_user_answer_by_page(uid, page_num):
    answers = db_answers.Answers().get_answers_by_uid_and_page(uid=uid, page_num=page_num, page_size=15)
    datas = []
    for answer in answers:
        data = {
            'question_id': answer.question_id,
            'title': db_questions.Questions().get_question_title_by_question_id(answer.question_id),
            'agree_count': answer.agree_count,
            'content': answer.content
        }
        datas.append(data)
    return json.dumps(datas, ensure_ascii=False)


@app.route('/api/user_focus_question/<int:uid>/page/<int:page_num>.json', methods=['POST', 'GET'])
def get_user_focus_question_by_page(uid, page_num):
    focus_questions = db_question_focus.Question_focus().get_focus_questions_by_uid_and_page(uid=uid, page_num=page_num,
                                                                            page_size=15)
    datas = []
    for focus_question in focus_questions:
        data = {
            'question_id': focus_question.question_id,
            'title': db_questions.Questions().get_question_title_by_question_id(focus_question.question_id),
            'username': db_users.Users().get_user_by_id(focus_question.uid).username,
            'is_anonymous': db_questions.Questions().get_question_by_id(focus_question.question_id).is_anonymous,
            'question_focus_count': db_question_focus.Question_focus().get_question_foucs_count(focus_question.question_id),
            'question_answer_count': db_answers.Answers().get_answer_count(focus_question.question_id),
            'question_view_count': db_questions.Questions().get_question_view_count(focus_question.question_id),
            'publish_time': timestamp_datetime(db_questions.Questions().get_question_by_id(focus_question.question_id).publish_time),
            'user_url': get_user_url(focus_question.question_id),
            'dynamic_str': get_dynamic_str(focus_question.question_id),
            'avatar_url': db_users.Users().get_user_by_id(db_questions.Questions().get_question_by_id(focus_question.question_id).questioner_uid).avatar_url
        }
        datas.append(data)
    return json.dumps(datas, ensure_ascii=False)


@app.route('/api/user_latest_activity/<int:uid>/page/<int:page_num>.json', methods=['POST', 'GET'])
def get_user_latest_activity_by_page(uid, page_num):
    from utils import get_user_latest_activity_datas_by_page
    latest_activity_datas = get_user_latest_activity_datas_by_page(username=db_users.Users().get_username_by_uid(uid), page_num=page_num, page_size=15)
    return json.dumps(latest_activity_datas, ensure_ascii=False)


@app.route('/api/dynamic/<int:uid>/page/<int:page_num>.json', methods=['GET', 'POST'])
def get_dynamic_datas_by_page_api(page_num, uid):
    return json.dumps(get_dynamic_datas_by_page(page_num=page_num, page_size=10, uid=uid), ensure_ascii=False)
