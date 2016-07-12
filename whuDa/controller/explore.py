# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template, redirect
from utils import is_login
import sys

reload(sys)
sys.setdefaultencoding('utf8')


@app.route('/')
def index():
    if is_login():
        return render_template('login/login-discover.html')
    return render_template('index.html')


@app.route('/dynamic')
def dynamic():
    if is_login():
        return render_template('login/login-dynamic.html')
    return redirect('/')


@app.route('/topic')
def topic():
    if is_login():
        return render_template('login/login-topic.html')
    return render_template('topic.html')


@app.route('/topic/<topic_name>')
def topic_detail(topic_name):
    if is_login():
        return render_template('login/login-topic_detail.html')
    return render_template('topic_detail.html')


@app.route('/notifications')
def notifications():
    if is_login():
        return render_template('login/notifications.html')
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


@app.route('/topic-recent-week')
def topic_recent_week():
    if is_login():
        return render_template('login/login-recent_week_topics.html')
    return render_template('recent_week_topics.html')


@app.route('/topic-recent-month')
def topic_recent_month():
    if is_login():
        return render_template('login/login-recent_month_topics.html')
    return render_template('recent_month_topics.html')


@app.route('/hot')
def hot():
    if is_login():
        return render_template('login/login-hot_questions.html')
    return render_template('hot_questions.html')


@app.route('/wait-reply')
def wait_reply():
    if is_login():
        return render_template('login/login-wait_reply.html')
    return render_template('wait_reply.html')


@app.route('/question/<int:id>')
def question(id):
    if is_login():
        return render_template('login/login-question_detail.html')
    return render_template('question_detail.html')


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

