# _*_ coding:utf8 _*_
from flask import session
from re import match
from time import time
from math import ceil
import whuDa.model.questions as db_questions
import whuDa.model.users as db_users
import whuDa.model.question_focus as db_question_focus
import whuDa.model.answers as db_answers
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def is_login():
    if 'username' in session:
        return True
    return False


def check_mail(email):
    if match('[a-zA-Z0-9_.-]*@[a-zA-Z0-9._-]', email, 0):
        return True
    return False


def check_username(username):
    if match('[a-zA-Z](.*)', username, 0):
        return True
    return False


# 根据时间戳获取过去的天数
def get_past_time(publish_time):
    past_time = int(time() - publish_time)
    if past_time / 60 == 0:
        return '%s秒' % past_time
    elif past_time / 3600 == 0:
        return '%s分钟' % str(int(past_time/60))
    elif past_time / (3600*24) == 0:
        return '%s小时' % str(int(past_time/3600))
    else:
        return '%s天' % str(int(past_time/(3600*24)))


# 获取最新动态的字符串（XXX发起了问题/XXX回答了问题）
def get_dynamic_str(question_id):
    # 判断是否有人回答
    if not db_answers.Answers().get_answer_count(question_id):
        # 是否匿名
        if db_questions.Questions().get_question_by_id(question_id).is_anonymous:
            return '匿名用户 发起了问题'
        return db_users.Users().get_username_by_uid(db_questions.Questions().get_questioner_uid(question_id)) + ' 发起了问题'
    else:
        # 获取最新的回答
        if db_answers.Answers().get_last_answer(question_id).is_anonymous:
            return '匿名用户 回答了问题'
        return db_users.Users().get_username_by_uid(db_answers.Answers().get_last_answer_uid(question_id)) + ' 回答了问题'

def get_user_url(question_id):
    # 判断是否有人回答
    if not db_answers.Answers().get_answer_count(question_id):
        # 是否匿名
        if db_questions.Questions().get_question_by_id(question_id).is_anonymous:
            return ''
        return '/' + db_users.Users().get_username_by_uid(db_questions.Questions().get_questioner_uid(question_id))
    else:
        # 获取最新的回答
        if db_answers.Answers().get_last_answer(question_id).is_anonymous:
            return ''
        return '/' + db_users.Users().get_username_by_uid(db_answers.Answers().get_last_answer_uid(question_id))


# 获取发现页面需要渲染的数据
def get_discover_datas(page_num, page_size):
    questions = db_questions.Questions().get_questions_by_page(page_num=page_num, page_size=page_size)
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
            'past_time': get_past_time(question.publish_time),
            'avatar_url': db_users.Users().get_user_by_id(question.questioner_uid).avatar_url,
            'dynamic_str': get_dynamic_str(question.question_id),
            'user_url': get_user_url(question.question_id)
        }
        datas.append(data)
    return datas


# 生成分页html
def page_html(total_count, page_size, current_page, url):
    # url类似 discover/page
    page_count = ceil(float(total_count) / page_size)
    result = ''
    if current_page - 3 > 1:
        result += '<li><a href="/' + url + '/1">&lt;&lt;</a></li>'
        result += '<li><a href="/' + url + '/' + str(current_page - 1) + '">&lt;</a></li>'
    for i in range(7):
        temp_page = current_page + (i-3)
        if 0 < temp_page <= page_count:
            if temp_page == current_page:
                result += '<li class="active"><a href="/' + url + '/' + str(temp_page) + '">' + str(temp_page) + '</a></li>'
            else:
                result += '<li><a href="/' + url + '/' + str(temp_page) + '">' + str(temp_page) + '</a></li>'
    if current_page + 3 < page_count:
        result += '<li><a href="/' + url + '/' + str(current_page + 1) + '">&gt;</a></li>'
        result += '<li><a href="/' + url + '/' + str(page_count) + '">&lt;&lt;</a></li>'
    return result
