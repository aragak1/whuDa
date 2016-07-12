drop database whuDa;
create database whuDa;
use whuDa;

create table users(
    uid int(11) unsigned not null auto_increment comment '用户的UID',
    username varchar(255) not null comment '用户名',
    password varchar(32) not null comment '密码',
    sex tinyint(1) default null comment '性别, 1代表男',
    birthday int(10) default null comment '生日',
    department_id int(10) default 0 comment '院系ID',
    introduction varchar(255) default null comment '个人简介',
    email varchar(255) not null comment 'email',
    qq varchar(16) default null comment 'QQ',
    phone varchar(16) default null comment '手机号码',
    website varchar(255) default null comment '个人网址',
    view_count int(10) not null default 0 comment '主页被浏览次数',
    agree_count int(10) not null default 0 comment '赞同数量',
    group_id tinyint(1) not null default 2 comment '用户组，0为管理员，1为普通用户，2为带审核用户',
    notification_unread int(11) not null default 0 comment '未读系统通知',
    message_unread int(11) not null default 0 comment '未读私信',
    invite_count int(10) not null default 0 comment '邀请数量',
    question_count int(10) not null default 0 comment '问题数量',
    answer_count int(10) not null default 0 comment '回答数量',
    topic_focus_count int(10) not null default 0 comment '关注的话题数量',
    reg_time int(10) default null comment '注册时间',
    last_login int(10) default null comment '上次登录时间',
    last_ip varchar(255) default null comment '上次登录IP',
    forbidden tinyint(1) default 0 comment '是否被禁止',
    primary key (uid)
) default charset=utf8;

create table questions(
    question_id int(11) unsigned not null auto_increment comment '问题ID',
    questioner_uid int(11) not null comment '提问者UID',
    title varchar(255) not null default '' comment '问题标题',
    content text not null comment '问题描述',
    publish_time int(10) not null comment '发布时间',
    update_time int(10) not null comment '最近修改时间',
    is_anonymous tinyint(1) not null default 0 comment '是否匿名',
    view_count int(10) not null default 0 comment '浏览次数',
    is_lock tinyint(1) not null default 0 comment '问题是否被锁定',
    primary key (question_id)
) default charset=utf8;

create table answers(
    answer_id int(11) unsigned not null auto_increment comment '回答ID',
    question_id int(11) not null comment '所回答问题的ID',
    answer_uid int(11) not null comment '回答用户的UID',
    content text not null comment '回答内容',
    is_anonymous tinyint(1) not null default 0 comment '是否匿名',
    answer_time int(10) not null comment '回答时间',
    agree_count int(10) not null default 0 comment '赞同数',
    disagree_count int(10) not null default 0 comment '反对数',
    primary key (answer_id)
) default charset=utf8;

create table answer_comments(
    id int(11) unsigned not null auto_increment comment '自增主键',
    answer_id int(11) not null comment '问题ID',
    content text not null comment '评论内容',
    uid int(11) not null comment '评论者UID',
    publish_time int(10) not null comment '评论时间',
    primary key (id)
) default charset=utf8;

create table answer_agree(
    id int(11) unsigned not null auto_increment comment '自增主键',
    question_id int(11) not null comment '赞同问题的ID',
    answer_id int(11) not null comment '被赞回答的ID',
    agree_uid int(11) not null comment '被赞用户的UID',
    uid int(11) not null comment '赞同用户的UID',
    primary key (id)
) default charset=utf8;

create table answer_disagree(
    id int(11) unsigned not null auto_increment comment '自增主键',
    question_id int(11) not null comment '反对问题的ID',
    answer_id int(11) not null comment '被反对回答的ID',
    disagree_uid int(11) not null comment '被反对用户的UID',
    uid int(11) not null comment '反对用户UID',
    primary key (id)
) default charset=utf8;

create table topics(
    topic_id int(11) unsigned not null auto_increment comment '话题ID',
    name varchar(32) not null comment '话题名字',
    introducation text comment '话题介绍',
    primary key (topic_id)
) default charset=utf8;

create table topic_question(
    id int(11) unsigned not null auto_increment comment '自增主键',
    topic_id int(11) not null comment '问题所属话题ID',
    question_id int(11) not null comment '问题ID',
    primary key (id)
) default charset=utf8;

create table topic_focus(
    id int(11) unsigned not null auto_increment comment '自增主键',
    uid int(11) not null comment '关注话题的用户UID',
    topic_id int(11) not null comment '关注的话题ID',
    primary key (id)
) default charset=utf8;

create table question_focus(
    id int(11) unsigned not null auto_increment comment '自增主键',
    uid int(11) not null comment '关注问题的用户UID',
    question_id int(11) not null comment '关注的问题ID',
    current_answer_count int(10) not null comment '关注时有的回答数',
    primary key (id)
) default charset=utf8;

create table department(
    department_id int(10) not null auto_increment comment '学院ID',
    name varchar(32) not null comment '学院名',
    primary key (department_id)
) default charset=utf8;

create table notification (
    notification_id int(11) unsigned not null auto_increment comment '通知ID',
    sender_uid int(11) not null comment '发送者UID',
    recipient_uid int(11) not null comment '接受者UID',
    content text not null comment '通知内容',
    send_time int(10) not null comment '发送时间',
    is_read tinyint(1) not null default 0 comment '是否已读',
    primary key (notification_id)
) default charset=utf8;

create table message(
    message_id int(11) unsigned not null auto_increment comment '私信ID',
    session_id int(11) not null comment '会话ID',
    sender_uid int(11) not null comment '发送者UID',
    recipient_uid int(11) not null comment '接受者UID',
    content text not null comment '私信内容',
    send_time int(10) not null comment '发送时间',
    is_read tinyint(1) not null default 0 comment '是否已读',
    primary key (message_id)
) default charset=utf8;

create table question_invite(
    question_invite_id int(11) unsigned not null auto_increment comment '邀请ID',
    question_id int(11) not null comment '邀请回答的问题ID',
    sender_uid int(11) not null comment '发送邀请的用户UID',
    recipient_uid int(11) not null comment '被邀请的用户UID',
    send_time int(10) not null comment '邀请发送时间',
    primary key(question_invite_id)
) default charset=utf8;

create table question_favorite(
    question_favorite_id int(11) unsigned not null auto_increment comment '收藏的ID',
    uid int(11) not null comment '收藏问题的用户UID',
    question_id int(11) not null comment '收藏的问题ID',
    add_time int(10) not null comment '收藏时间',
    primary key (question_favorite_id)
) default charset=utf8;

create table topic_recommend(
    id int(11) unsigned not null auto_increment comment '自增主键',
    recommend_time int(10) not null comment '推荐时间',
    topic_id int(11) not null comment '推荐的话题ID',
    primary key (id)
) default charset=utf8;

insert into department(department_id, name) values
(1, '哲学学院'),
(2, '国学院'),
(3, '文学院'),
(4, '外国语言文学学院'),
(5, '新闻与传播学院'),
(6, '艺术学系'),
(8, '经济与管理学院'),
(9, '法学院'),
(10, '马克思主义学院'),
(11, '社会学系'),
(12, '政治与公共管理学院'),
(13, '教育科学研究院'),
(14, '信息管理学院'),
(15, '国际教育学院'),
(16, '数学与统计学院'),
(17, '物理科学与技术学院'),
(18, '化学与分子科学学院'),
(19, '生命科学学院'),
(20, '资源与环境科学学院'),
(21, '动力与机械学院'),
(22, '电气工程学院'),
(23, '城市设计学院'),
(24, '土木建筑工程学院'),
(25, '水利水电学院'),
(26, '电子信息学院'),
(27, '计算机学院'),
(28, '国际软件学院'),
(29, '测绘学院'),
(30, '遥感信息工程学院'),
(31, '印刷与包装系'),
(32, '医学部机关'),
(33, '基础医学院'),
(34, '公共卫生学院'),
(35, '第一临床医学院'),
(36, '第二临床医学院'),
(37, '口腔医学院'),
(38, 'HOPE护理学院'),
(39, '药学院'),
(40, '医学职业技术学院');
