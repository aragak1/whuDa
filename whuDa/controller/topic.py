# _*_ coding: utf8 _*_
from whuDa import app
from utils import is_login, page_html,  get_topic_detail_question_datas, timestamp_datetime
from flask import render_template, session
from time import time
import whuDa.model.topic_question as db_topic_question
import whuDa.model.users as db_users
import whuDa.model.topics as db_topics
import whuDa.model.topic_recommend as db_topic_recommend
import whuDa.model.topic_focus as db_topic_focus


@app.route('/topic')
def topic():
    datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15)
    today_topic = db_topics.Topics().get_topic_by_id(
        db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
    pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                           page_size=15,
                           current_page=1,
                           url='topic/page')
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])

        return render_template('login/login-topic.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               today_topic=today_topic)
    return render_template('topic.html',
                           datas=datas,
                           pagination=pagination,
                           today_topic=today_topic)


@app.route('/topic/page/<int:page_num>')
def get_page_topic(page_num):
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=page_num, page_size=15)
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=page_num,
                               url='topic/page')
        today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        return render_template('login/login-topic.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic/page',
                               today_topic=today_topic)
    return render_template('topic.html')


@app.route('/topic-recent-week')
def topic_recent_week():
    datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15, last_week=True)
    pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                           page_size=15,
                           current_page=1,
                           url='topic/page')
    today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-recent_week_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-week/page',
                               today_topic=today_topic)
    return render_template('recent_week_topics.html',
                           datas=datas,
                           pagination=pagination,
                           url='topic-recent-week/page',
                           today_topic=today_topic)


@app.route('/topic-recent-week/page/<int:page_num>')
def topic_recent_week_page(page_num):
    datas = db_topics.Topics().get_topics_by_page(page_num=page_num, page_size=15, last_week=True)
    pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                           page_size=15,
                           current_page=page_num,
                           url='topic-recent-week/page')
    today_topic = db_topics.Topics().get_topic_by_id(
        db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())

    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-recent_week_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic/page',
                               today_topic=today_topic)
    return render_template('login/login-recent_week_topics.html',
                           datas=datas,
                           pagination=pagination,
                           url='topic/page',
                           today_topic=today_topic)


@app.route('/topic-recent-month')
def topic_recent_month():
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15, last_month=True)
    pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                           page_size=15,
                           current_page=1,
                           url='topic/page')
    today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-recent_month_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-month/page',
                               today_topic=today_topic)
    return render_template('recent_month_topics.html',
                           datas=datas,
                           pagination=pagination,
                           url='topic-recent-month/page',
                           today_topic=today_topic)


@app.route('/topic-recent-month/page/<int:page_num>')
def topic_recent_month_page(page_num):
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    datas = db_topics.Topics().get_topics_by_page(page_num=page_num, page_size=15, last_month=True)
    pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                           page_size=15,
                           current_page=page_num,
                           url='topic/page')
    today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-recent_month_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-month/page',
                               today_topic=today_topic)
    return render_template('recent_month_topics.html')


# 话题的详细页面
@app.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    topic = db_topics.Topics().get_topic_by_id(topic_id)
    first_page_datas = get_topic_detail_question_datas(page_num=1, page_size=15, topic_id=topic_id)
    focus_count = db_topic_focus.Topic_focus().get_foucs_count(topic_id)
    focus_users = db_topics.Topics().get_focus_users(topic_id)
    question_count = db_topic_question.Topic_question().get_question_count(topic_id)
    c_time = timestamp_datetime(time())
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/login-topic_detail.html',
                               user=user,
                               topic=topic,
                               datas=first_page_datas,
                               focus_count=focus_count,
                               focus_users=focus_users,
                               question_count=question_count,
                               c_time=c_time)
    return render_template('topic_detail.html')
