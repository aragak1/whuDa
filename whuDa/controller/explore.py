# _*_ coding:utf8 _*_
import sys
import json
from time import time
from flask import render_template, redirect, session, request
import whuDa.model.department as db_department
import whuDa.model.questions as db_questions
import whuDa.model.topic_focus as db_topic_focus
import whuDa.model.topics as db_topics
import whuDa.model.users as db_users
import whuDa.model.notification as db_notification
import whuDa.model.question_focus as db_question_focus
import whuDa.model.message as db_message
from utils import is_login, get_discover_datas, page_html, get_hot_datas, get_wait_reply_datas, get_date
from whuDa import app
from utils import get_user_answer_datas, get_user_question_datas, get_user_focus_question_datas, get_user_latest_activity_datas
from utils import get_user_focus_questions_list_datas, get_dynamic_datas_by_page
from utils import get_notification_data

reload(sys)
sys.setdefaultencoding('utf8')


# 登陆前后的index页面都是发现页面
@app.route('/')
def index():
    db_topics.Topics().get_topics_by_page(1, 1)
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='discover/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        focus_topics = db_topic_focus.Topic_focus().get_user_focus_topics(user.uid)
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html',
                           datas=get_discover_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


@app.route('/discover/page/<int:page_num>')
def discover(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='discover/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        focus_topics = db_topic_focus.Topic_focus().get_user_focus_topics(user.uid)
        return render_template('login/login-discover.html',
                               user=user,
                               datas=get_discover_datas(page_num=page_num, page_size=15),
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users,
                               focus_topics=focus_topics)
    return render_template('index.html',
                           datas=get_discover_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


@app.route('/hot/page/<int:page_num>')
def hot_page(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='hot/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=page_num, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('hot_questions.html',
                           datas=get_hot_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


@app.route('/wait-reply/page/<int:page_num>')
def wait_reply_page(page_num):
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                           page_size=15,
                           current_page=page_num,
                           url='wait-reply/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=page_num, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html',
                           datas=get_wait_reply_datas(page_num=page_num, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


@app.route('/dynamic')
def dynamic():
    if is_login():
        hot_users = db_users.Users().get_top3_users()
        user = db_users.Users().get_user(session['username'])
        datas = get_dynamic_datas_by_page(page_num=1, page_size=10, uid=user.uid)
        topics = db_topics.Topics().get_3_topics(user.uid)
        return render_template('login/login-dynamic.html',
                               user=user,
                               datas=datas,
                               hot_users=hot_users,
                               topics=topics)
    return redirect('/')


@app.route('/notifications', methods=['GET', 'POST'])
def show_notifications():
    if request.method == 'GET' and is_login():
        user = db_users.Users().get_user(session['username'])
        uid = db_users.Users().get_uid_by_username(session['username'])
        temp_notifications = db_notification.Notification().get_notification_by_ruid(uid)
        unread = 0
        notifications = []
        more = 0
        page = 1
        for notification in temp_notifications:
            if notification.is_read == 0:
                unread += 1
            sender = db_users.Users().get_user_by_id(notification.sender_uid)
            question = db_questions.Questions().get_question_by_id(int(notification.content[0:1]))
            sender_notification_question = {
                'notification_id': notification.notification_id,
                'sender_uid': sender.uid,
                'sender_name': sender.username,
                'content': notification.content,
                'question_id': question.question_id,
                'question_title': question.title,
                'is_read': notification.is_read}
            notifications.append(sender_notification_question)
        if len(notifications) > 5:
            notifications = notifications[0:5]
            more = 1
        return render_template('login/notifications.html',
                               unread=unread,
                               notifications=notifications,
                               more=more,
                               page=page,
                               user=user)
    elif request.method == 'POST':
        option = request.form.get('option')
        if option == 'has_read':
            id = request.form.get('notification_id')
            return db_notification.Notification().has_read(id)
        elif option == 'delete':
            id = request.form.get('notification_id')
            return db_notification.Notification().delete(id)
    return redirect('/')


@app.route('/notifications/<int:page_num>')
def show_notifications_page(page_num):
    if is_login():
        uid = db_users.Users().get_uid_by_username(session['username'])
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
                'content': notification.content,
                'question_id': question.question_id,
                'question_title': question.title,
                'is_read': notification.is_read}
            notifications.append(sender_notification_question)
        if len(notifications) > 5 * (page_num + 1):
            notifications = notifications[0:5 * (page_num + 1)]
            more = 1
        else:
            more = 0
        page_num += 1
        return render_template('login/notifications.html',
                               unread=unread,
                               notifications=notifications,
                               more=more,
                               page=page_num)
    return redirect('/')


@app.route('/notifications.json', methods=['POST', 'GET'])
def get_more_notifications():
    if request.method == 'POST':

        page_num = int(request.form.get('page_num'))

        uid = db_users.Users().get_uid_by_username(session['username'])
        datas = get_notification_data(uid)
        if len(datas['notifications']) > 5 * (page_num + 1):
            datas['notifications'] = datas['notifications'][5*page_num:5 * (page_num + 1)]
            more = 1
        else:
            datas['notifications']=datas['notifications'][5*page_num:]
            more = 0
        page_num += 1
        datas['more'] = more
        datas['page_num'] = page_num
        return json.dumps(datas, ensure_ascii=False)
    else:
        return redirect('/')


@app.route('/message')
def message():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        message_datas = db_message.Message().get_messages(user.uid)
        return render_template('login/message.html',
                               user=user,
                               datas=message_datas)
    return redirect('/')


@app.route('/message/<int:session_id>')
def message_detail(session_id):
    if is_login():
        user = db_users.Users().get_user(session['username'])
        if db_message.Message().is_user_session(session_id, user.uid):
            message_datas = db_message.Message().get_messages_by_session_id(session_id)
            return render_template('login/message_detail.html',
                                   user=user,
                                   datas=message_datas,
                                   session_id=session_id)
        return redirect('/')
    return redirect('/')


@app.route('/message/send', methods=['GET', 'POST'])
def send_message():
    if is_login():
        sender = db_users.Users().get_user(session['username'])
        recipient_name = request.form.get('recipient')
        recipient = db_users.Users().get_user(recipient_name)
        session_id = int(request.form.get('session_id'))
        content = request.form.get('content')
        if not content:
            return 'empty_content'
        db_message.Message().send_message(session_id=session_id,
                                          sender_uid=sender.uid,
                                          recipient_uid=recipient.uid,
                                          content=content)
        return 'success'
    return redirect('/')


@app.route('/help')
def help():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-help.html',
                               user=user)
    return render_template('help.html')


@app.route('/about')
def about():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-about.html',
                               user=user)
    return render_template('about.html')


@app.route('/setting')
def setting():
    if is_login():
        dates = {
            'year': [y for y in range(1900, 1+get_date(time())['year'])],
            'month': [m for m in range(1, 13)],
            'day': [d for d in range(1, 32)]}
        birthday = db_users.Users().get_birthday_dict(db_users.Users().get_uid_by_username(session['username']))
        departments = db_department.Department().get_all_department()
        user = db_users.Users().get_user(session['username'])
        return render_template('login/user_setting.html',
                               user=user,
                               departments=departments,
                               dates=dates,
                               birthday=birthday)
    return redirect('/')


@app.route('/hot')
def hot():
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='hot/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-hot_questions.html',
                               user=user,
                               datas=get_hot_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_topics=hot_topics,
                               hot_users=hot_users)
    return render_template('hot_questions.html',
                           datas=get_hot_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_topics=hot_topics,
                           hot_users=hot_users)


@app.route('/wait-reply')
def wait_reply():
    hot_topics = db_topics.Topics().get_top5_topics()
    hot_users = db_users.Users().get_top5_users()
    pagination = page_html(total_count=db_questions.Questions().get_wait_reply_questions_count(),
                           page_size=15,
                           current_page=1,
                           url='wait-reply/page')
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-wait_reply.html',
                               user=user,
                               datas=get_wait_reply_datas(page_num=1, page_size=15),
                               pagination=pagination,
                               hot_users=hot_users,
                               hot_topics=hot_topics)
    return render_template('wait_reply.html',
                           datas=get_wait_reply_datas(page_num=1, page_size=15),
                           pagination=pagination,
                           hot_users=hot_users,
                           hot_topics=hot_topics)


# 需要一个user，一个people，5条回复，5条提问，5个动态，关注话题，关注的问题
# question的reply_count手动计算
# question的focus_count手动计算
# 动态的所有数据都要手动计算
# 关注的话题涉及topic_focus和topics的连接查询
@app.route('/people/<name>')
def people(name):
    people = db_users.Users().get_user(username=name)
    temp_answer_datas = get_user_answer_datas(name)
    temp_question_datas = get_user_question_datas(name)
    temp_focus_topic_datas = db_topic_focus.Topic_focus().get_user_focus_topics(db_users.Users().get_uid_by_username(name))
    temp_focus_question_datas = get_user_focus_question_datas(name)
    temp_latest_activity_datas = get_user_latest_activity_datas(username=name)
    temp_question_list_datas = temp_question_datas
    temp_answer_list_datas = temp_answer_datas
    focus_question_list_datas = get_user_focus_questions_list_datas(people.uid)
    temp_latest_activity_list_datas = temp_latest_activity_datas
    if len(temp_answer_datas) > 5:
        answer_datas = temp_answer_datas[0:5]
    else:
        answer_datas = temp_answer_datas
    if len(temp_question_datas) > 5:
        question_datas = temp_question_datas[0:5]
    else:
        question_datas = temp_question_datas
    if len(temp_focus_topic_datas) > 5:
        focus_topic_datas = temp_focus_topic_datas[0:5]
    else:
        focus_topic_datas = temp_focus_topic_datas
    if len(temp_focus_question_datas) > 5:
        focus_question_datas = temp_focus_question_datas[0:5]
    else:
        focus_question_datas = temp_focus_question_datas
    if len(temp_latest_activity_datas) > 5:
        latest_activity_datas = temp_latest_activity_datas[0:5]
    else:
        latest_activity_datas = temp_latest_activity_datas
    if len(temp_question_list_datas) > 15:
        question_list_datas = temp_question_list_datas[0:15]
    else:
        question_list_datas = temp_question_list_datas
    if len(temp_answer_list_datas) > 15:
        answer_list_datas = temp_answer_list_datas[0:15]
    else:
        answer_list_datas = temp_answer_list_datas
    if len(temp_latest_activity_list_datas) > 15:
        latest_activity_list_datas = temp_latest_activity_list_datas[0:15]
    else:
        latest_activity_list_datas = temp_latest_activity_list_datas
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-person_detail.html',
                               user=user,
                               people=people,
                               answer_datas=answer_datas,
                               question_datas=question_datas,
                               latest_activity_datas=latest_activity_datas,
                               focus_topic_datas=focus_topic_datas,
                               focus_question_datas=focus_question_datas,
                               question_focus_count=db_question_focus.Question_focus().get_user_focus_question_count(name),
                               question_list_datas=question_list_datas,
                               answer_list_datas=answer_list_datas,
                               focus_question_list_datas=focus_question_list_datas,
                               latest_activity_list_datas=latest_activity_list_datas)
    return render_template('person_detail.html',
                           people=people,
                           answer_datas=answer_datas,
                           question_datas=question_datas,
                           latest_activity_datas=latest_activity_datas,
                           focus_topic_datas=focus_topic_datas,
                           focus_question_datas=focus_question_datas,
                           question_focus_count=db_question_focus.Question_focus().get_user_focus_question_count(name),
                           question_list_datas=question_list_datas,
                           answer_list_datas=answer_list_datas,
                           focus_question_list_datas=focus_question_list_datas,
                           latest_activity_list_datas=latest_activity_list_datas)


@app.route('/all_users/page/<int:page_num>')
def all_users_page(page_num):
    user = db_users.Users().get_user(session['username'])
    pagination = page_html(total_count=db_users.Users().get_users_count(),
                           page_size=15,
                           current_page=page_num,
                           url='all_users/page')
    return render_template('login/all_users.html',
                           user=user,
                           all_users_datas=db_users.Users().get_all_users(),
                           pagination=pagination)


@app.route('/all_users')
def all_users():
    user = db_users.Users().get_user(session['username'])
    pagination = page_html(total_count=db_users.Users().get_users_count(),
                           page_size=15,
                           current_page=1,
                           url='all_users/page')
    return render_template('login/all_users.html',
                           user=user,
                           all_users_datas=db_users.Users().get_all_users(),
                           pagination=pagination)

