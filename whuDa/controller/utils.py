# _*_ coding:utf8 _*_
from flask import session
from re import match
from time import time, strftime, localtime, strptime, mktime
from math import ceil
from PIL import Image
import whuDa.model.questions as db_questions
import whuDa.model.users as db_users
import whuDa.model.question_focus as db_question_focus
import whuDa.model.answers as db_answers
import whuDa.model.notification as db_notification
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


def get_avatar_url(question_id):
    # 判断是否有人回答
    if not db_answers.Answers().get_answer_count(question_id):
        # 是否匿名
        if db_questions.Questions().get_question_by_id(question_id).is_anonymous:
            return '/static/img/avatar/avatar.png'
        return '/' + db_users.Users().get_user_by_id(db_questions.Questions().get_questioner_uid(question_id)).avatar_url
    else:
        # 获取最新的回答
        if db_answers.Answers().get_last_answer(question_id).is_anonymous:
            return '/static/img/avatar/avatar.png'
        return '/' + db_users.Users().get_user_by_id(db_answers.Answers().get_last_answer_uid(question_id)).avatar_url


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
            'avatar_url': get_avatar_url(question.question_id),
            'dynamic_str': get_dynamic_str(question.question_id),
            'user_url': get_user_url(question.question_id)
        }
        datas.append(data)
    return datas


# 获取热门问题页面需要渲染的数据
def get_hot_datas(page_num, page_size):
    questions = db_questions.Questions().get_hot_questions_by_page(page_num=page_num, page_size=page_size)
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


# 获取等待回复页面需要渲染的数据
def get_wait_reply_datas(page_num, page_size):
    questions = db_questions.Questions().get_wait_reply_questions_by_page(page_num=page_num, page_size=page_size)
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


# unix时间戳转日期
def timestamp_datetime(unix_time):
    format = '%Y-%m-%d %H:%M:%S'
    return strftime(format, localtime(unix_time))


# birthday转时间戳
def birthday_to_unix_time(year, month, day):
    birth_str = '{}-{}-{} {}'.format(year, month, day, '8')
    return int(mktime(strptime(birth_str, '%Y-%m-%d %H')))


# 获取年月日的dict
def get_date(unix_time):
    date = {
        'year': int(strftime('%Y', localtime(unix_time))),
        'month': int(strftime('%m', localtime(unix_time))),
        'day': int(strftime('%d', localtime(unix_time))),
        'hour': int(strftime('%H', localtime(unix_time))),
        'minute': int(strftime('%M', localtime(unix_time))),
        'secnod': int(strftime('%S', localtime(unix_time)))
    }
    return date


# 获取某个话题下面需要渲染的问题数据
def get_topic_detail_question_datas(page_num, page_size, topic_id):
    datas = []
    questions = db_questions.Questions().get_questions_by_topic_id_and_page(topic_id=topic_id,
                                                                            page_num=page_num,
                                                                            page_size=page_size)
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


# 获取一个用户的回答和回答对应的问题，用于用户主页的回复部分的渲染
def get_user_answer_datas(username):
    datas = []
    answers = db_answers.Answers().get_user_answers_with_question(username=username)
    for answer in answers:
        data = {
            'question_id': answer.question_id,
            'title': db_questions.Questions().get_question_title_by_question_id(answer.question_id),
            'agree_count': answer.agree_count,
            'content': answer.content
        }
        datas.append(data)
    return datas


# 获取一个用户的提出的问题，用户用户主页的提问部分的渲染
def get_user_question_datas(username):
    datas = []
    questions = db_questions.Questions().get_user_questions(username=username)
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
    return datas


# 获取一个用户的回复的由新到旧排序的数据
def get_user_answers_order_by_time(username):
    datas = []
    answers = db_answers.Answers().get_user_answers_order_by_time(username=username)
    for answer in answers:
        data = {
            'last_time': answer.answer_time,
            'question_id': answer.question_id,
            'title': db_questions.Questions().get_question_title_by_question_id(answer.question_id)
        }
        datas.append(data)
    return datas


# 获取一个用户的提问的由新到旧排序的数据
def get_user_questions_order_by_time(username):
    datas = []
    questions = db_questions.Questions().get_questions_order_by_time(username=username)
    for question in questions:
        data = {
            'last_time': question.publish_time,
            'question_id': question.question_id,
            'title': question.title
        }
        datas.append(data)
    return datas


# 获取一个用户所关注的问题的数据
def get_user_focus_question_datas(username):
    datas = []
    focus_questions = db_question_focus.Question_focus().get_user_focus_questions(username)
    for focus_question in focus_questions:
        data = {
            'question_id': focus_question.question_id,
            'title': db_questions.Questions().get_question_title_by_question_id(focus_question.question_id)
        }
        datas.append(data)
    return datas


# 获取一个用户的最新动态的数据（回复和提问的综合)
def get_user_latest_activity_datas(username):
    datas = []
    latest_answer_datas = get_user_answers_order_by_time(username)
    latest_question_datas = get_user_questions_order_by_time(username)
    len1 = len(latest_answer_datas)
    len2 = len(latest_question_datas)
    x = 0
    j = 0
    for i in range(1, len1 + len2 + 1):
        if x <= len1 - 1 and j <= len2 - 1:
            if latest_answer_datas[x]['last_time'] > latest_question_datas[j]['last_time']:
                is_question = 0
                question_id = latest_answer_datas[x]['question_id']
                title = db_questions.Questions().get_question_title_by_question_id(question_id)
                last_time = get_past_time(latest_answer_datas[x]['last_time'])
                x += 1
            else:
                is_question = 1
                question_id = latest_question_datas[j]['question_id']
                title = latest_question_datas[j]['title']
                last_time = get_past_time(latest_question_datas[j]['last_time'])
                j += 1
        elif x > len1 - 1 and j <= len2 - 1:
            is_question = 1
            question_id = latest_question_datas[j]['question_id']
            title = latest_question_datas[j]['title']
            last_time = get_past_time(latest_question_datas[j]['last_time'])
            j += 1
        elif x <= len1 - 1 and j >= len2 - 1:
            is_question = 0
            question_id = latest_answer_datas[x]['question_id']
            title = db_questions.Questions().get_question_title_by_question_id(question_id)
            last_time = get_past_time(latest_answer_datas[x]['last_time'])
            x += 1
        else:
            pass
        data = {
            'is_question': is_question,
            'question_id': question_id,
            'title': title,
            'last_time': last_time
        }
        datas.append(data)
    return datas


# 把图片缩放到指定大小
def resize_pic(pic_path, save_path, width, height):
    im = Image.open(pic_path)
    nim = im.resize((width, height), Image.BILINEAR)
    nim.save(save_path)


def get_user_focus_questions_list_datas(uid):
    focus_questions = db_question_focus.Question_focus().get_focus_questions_by_uid_and_page(uid=uid, page_num=1,
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
            'publish_time': timestamp_datetime(
                db_questions.Questions().get_question_by_id(focus_question.question_id).publish_time),
            'user_url': get_user_url(focus_question.question_id),
            'dynamic_str': get_dynamic_str(focus_question.question_id),
            'avatar_url': db_users.Users().get_user_by_id(
                db_questions.Questions().get_question_by_id(focus_question.question_id).questioner_uid).avatar_url
        }
        datas.append(data)
    return datas

#获取通知信息
def get_notification_data(uid):
    temp_notifications = db_notification.Notification().get_notification_by_ruid(uid)
    unread = 0
    notifications = []

    for notification in temp_notifications:
        if notification.is_read == 0:
            unread += 1
        sender = db_users.Users().get_user_by_id(notification.sender_uid)
        question = db_questions.Questions().get_question_by_id(int(notification.content[0:1]))
        sender_notification_question = {
            'notification_id': notification.notification_id,
            'sender_uid': sender.uid,
            'sender_name': sender.username,
            'content': notification.content[2:],
            'question_id': question.question_id,
            'question_title': question.title,
            'is_read': notification.is_read,
            'past_time':get_past_time(notification.send_time)}
        notifications.append(sender_notification_question)
    datas={'notifications':notifications,'unread':unread}
    return datas
#获取关注问题
def get_all_focus_data(uname):
    temp_all_focus = db_question_focus.Question_focus().get_user_focus_questions(uname)
    all_focus = []
    for focus in temp_all_focus:
        question = db_questions.Questions().get_question_by_id(focus.question_id)
        focus_questions = {
            'question_id':question.question_id,
            'username':session['username'],
            'question_name':question.title,
            'c_answer':focus.current_answer_count}
        all_focus.append(focus_questions)
    datas={'all_focus':all_focus}
    return datas

