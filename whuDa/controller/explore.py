# _*_ coding:utf8 _*_
import sys
import json

from flask import render_template, redirect, session,request

import whuDa.model.questions as db_questions
import whuDa.model.topic_focus as db_topic_focus
import whuDa.model.topics as db_topics
import whuDa.model.users as db_users
import whuDa.model.notification as db_notification
from utils import is_login, get_discover_datas, page_html, get_hot_datas, get_wait_reply_datas
from whuDa import app

reload(sys)
sys.setdefaultencoding('utf8')


'''
    渲染需要的数据:
    判断page，根据page返回问题的list
    问题标题，问题id （questions）
    问题的最新回复者/发起者 (user)
    问题关注人数 (question_focus)
    问题回复数 (answers)
    问题浏览次数 (questions)
    问题发布时间 (questions)
'''


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
                               pagenation=pagination,
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
        return render_template('login/login-dynamic.html')
    return redirect('/')

@app.route('/notifications', methods=['GET', 'POST'])
def show_notifications():
    if request.method == 'GET' and is_login():
        uid=db_users.Users().get_uid_by_username(session['username'])
        temp_notifications=db_notification.Notification().get_notification_by_ruid(uid)
        unread=0
        notifications=[]
        more=0
        page=1
        for notification in temp_notifications:
            if notification.is_read==0:
                unread += 1
            sender=db_users.Users().get_user_by_id(notification.sender_uid)
            question=db_questions.Questions().get_question_by_id(int(notification.content[0:1]))
            sender_notification_question={
                'notification_id':notification.notification_id,
                'sender_uid':sender.uid,
                'sender_name':sender.username,
                'content':notification.content,
                'question_id':question.question_id,
                'question_title':question.title,
                'is_read':notification.is_read}
            notifications.append(sender_notification_question)
        if len(notifications)>5:
            notifications=notifications[0:5]
            more=1
        return render_template('login/notifications.html',
                               unread=unread,
                               notifications=notifications,
                               more=more,
                               page=page)
    elif request.method == 'POST':
        option=request.form.get('option')
        if option=='has_read':
            id=request.form.get('notification_id')
            return db_notification.Notification().has_read(id)
        elif option=='delete':
            id=request.form.get('notification_id')
            return db_notification.Notification().delete(id)
    return redirect('/')

@app.route('/notifications/<int:page_num>')
def show_notifications_page(page_num):
    if is_login():
        uid=db_users.Users().get_uid_by_username(session['username'])
        temp_notifications=db_notification.Notification().get_notification_by_ruid(uid)
        unread=0
        notifications=[]
        for notification in temp_notifications:
            if notification.is_read==0:
                unread += 1
            sender=db_users.Users().get_user_by_id(notification.sender_uid)
            question=db_questions.Questions().get_question_by_id(int(notification.content[0:1]))
            sender_notification_question={
                'notification_id':notification.notification_id,
                'sender_uid':sender.uid,
                'sender_name':sender.username,
                'content':notification.content,
                'question_id':question.question_id,
                'question_title':question.title,
                'is_read':notification.is_read}
            notifications.append(sender_notification_question)
        if len(notifications) > 5 * (page_num + 1):
            notifications = notifications[0:5 * (page_num + 1)]
            more = 1
        else :
            more=0
        page_num=page_num+1
        return render_template('login/notifications.html',
                               unread=unread,
                               notifications=notifications,
                               more=more,
                               page=page_num)
    return redirect('/')

@app.route('/message')
def message():
    if is_login():
        return render_template('login/message.html')
    return redirect('/')

@app.route('/help')
def help():
    if is_login():
        return render_template('login/login-help.html')
    return render_template('help.html')


@app.route('/about')
def about():
    if is_login():
        return render_template('login/login-about.html')
    return render_template('about.html')


@app.route('/setting')
def setting():
    if is_login():
        return render_template('login/user_setting.html')
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


@app.route('/people/<name>')
def people(name):
    if is_login():
        return render_template('login/login-person_detail.html')
    return render_template('person_detail.html')


@app.route('/setting/security')
def change_pass():
    if is_login():
        return render_template('login/change_pass.html')
    return redirect('/')
