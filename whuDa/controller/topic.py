from whuDa import app
from utils import is_login, page_html
from flask import render_template, session
import whuDa.model.users as db_users
import whuDa.model.topics as db_topics
import whuDa.model.topic_recommend as db_topic_recommend


@app.route('/topic')
def topic():
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15)
        today_topic = db_topics.Topics().get_topic_by_id(
            db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=1,
                               url='topic/page')
        return render_template('login/login-topic.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               today_topic=today_topic)
    return render_template('topic.html')


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
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15, last_week=True)
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=1,
                               url='topic/page')
        today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        return render_template('login/login-recent_week_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-week/page',
                               today_topic=today_topic)
    return render_template('recent_week_topics.html')


@app.route('/topic-recent-week/page/<int:page_num>')
def topic_recent_week_page(page_num):
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=page_num, page_size=15, last_week=True)
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=page_num,
                               url='topic-recent-week/page')
        today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        return render_template('login/login-recent_week_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic/page',
                               today_topic=today_topic)
    return render_template('login/login-recent_week_topics.html')


@app.route('/topic-recent-month')
def topic_recent_month():
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=1, page_size=15, last_month=True)
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=1,
                               url='topic/page')
        today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        return render_template('login/login-recent_month_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-month/page',
                               today_topic=today_topic)
    return render_template('recent_month_topics.html')


@app.route('/topic-recent-month/page/<int:page_num>')
def topic_recent_month_page(page_num):
    db_topic_recommend.Topic_recommend().test_and_update_today_recommend_topic()
    if is_login():
        user = db_users.Users().get_user(session['username'])
        datas = db_topics.Topics().get_topics_by_page(page_num=page_num, page_size=15, last_month=True)
        pagination = page_html(total_count=db_topics.Topics().get_topic_count(),
                               page_size=15,
                               current_page=page_num,
                               url='topic/page')
        today_topic = db_topics.Topics().get_topic_by_id(db_topic_recommend.Topic_recommend().get_today_recommend_topic_id())
        return render_template('login/login-recent_month_topics.html',
                               user=user,
                               datas=datas,
                               pagination=pagination,
                               url='topic-recent-month/page',
                               today_topic=today_topic)
    return render_template('recent_month_topics.html')


@app.route('/topic/<topic_name>')
def topic_detail(topic_name):
    if is_login():
        return render_template('login/login-topic_detail.html')
    return render_template('topic_detail.html')