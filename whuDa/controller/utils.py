# _*_ coding:utf8 _*_
from flask import session
from re import match
from time import time
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
            'avatar_url': db_users.Users().get_user_by_id(question.questioner_uid).avatar_url
        }
        datas.append(data)
    return datas


# 生成分页html
def page_html():
    pass
