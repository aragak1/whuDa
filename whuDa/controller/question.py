# _*_ coding:utf8 _*_
from whuDa import app
from flask import request, redirect, render_template, session
from utils import is_login
import whuDa.model.questions as db_questions
import whuDa.model.topic_question as db_topic_questions
import whuDa.model.topics as db_topics
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

            return 'success'
        else:
            return 'error'
    return redirect('/')


@app.route('/publish/question', methods=['POST'])
def publish_question():
    if is_login():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            topics = request.form.getlist('topics[]')
            is_anonymous = int(request.form.get('anonymous'))
            if title == '':
                return 'empty_title'
            if not topics:
                return 'empty_topics'
            uid = db_users.Users().get_uid_by_username(session['username'])

            # 在question表中插入问题
            question_id = db_questions.Questions().publish(
                questioner_uid=uid,
                title=title,
                content=content,
                is_anonymous=is_anonymous)
            # 把问题所属的话题加入表中
            for topic in topics:
                topic_id = db_topics.Topics().get_topic_id_by_name(topic)
                db_topic_questions.Topic_question().add_to_topic(
                    question_id=question_id,
                    topic_id=topic_id)

            # 用户关注该问题
            db_question_focus.Question_focus().add_focus_question(uid=uid, question_id=question_id, cnt=1)

            # 用户问题数加一
            db_users.Users().add_answer_count(session['username'])
            return str(question_id)
    return redirect('/')


@app.route('/question/<int:id>')
def question(id):
    if is_login():
        user = db_users.Users().get_user(session['username'])
        question = db_questions.Questions().get_question_by_id(id)
        questioner = db_users.Users().get_user_by_id(uid=question.questioner_uid)
        question_focus_cnt = db_topic_questions.Topic_question().get_topics_by_id(question.question_id)
        if question:
            topics = db_topic_questions.Topic_question().get_topics_by_id(question_id=question.question_id)
            return render_template('login/login-question_detail.html',
                                   question=question,
                                   topics=topics,
                                   user=user,
                                   question_focus_cnt=question_focus_cnt,
                                   questioner=questioner)
        return '没有这个问题'
    return render_template('question_detail.html')



