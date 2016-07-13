# _*_ coding:utf8 _*_
from whuDa import app
from flask import request, redirect, render_template, session
from utils import is_login
import whuDa.model.questions as db_questions
import whuDa.model.question_focus as db_question_focus
import whuDa.model.users as db_users


''' 发布一个问题需要进行的操作：
    添加一个问题，
    发布者关注该问题，
    发布者的问题数加一，
    添加问题所属的话题记录
'''


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if is_login():
        user = db_users.Users().get_user(session['username'])
        return render_template('login/publish.html', user=user)
    return redirect('/')


@app.route('/publish/<int:question_id>', methods=['GET', 'POST'])
def update_question(question_id):
    if is_login():
        if request.method == 'POST':
            pass
        else:
            pass
    return redirect('/')


@app.route('/publish/question', methods=['GET', 'POST'])
def publish_question():
    if is_login() and request.method == 'POST':
        pass
    return redirect('/')



