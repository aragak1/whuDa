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
    avatar_url varchar(255) default 'static/img/avatar/avatar.png',
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
    answer_id int(11) not null comment '被赞回答的ID',
    agree_uid int(11) not null comment '赞用户的UID',
    primary key (id)
) default charset=utf8;

create table topics(
    topic_id int(11) unsigned not null auto_increment comment '话题ID',
    name varchar(32) not null comment '话题名字',
    introducation text comment '话题介绍',
    topic_url varchar(255) default 'static/img/topic/topic.png',
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

insert into topics(name, introducation) values
('bug', '英文单词，本意是臭虫、缺陷、损坏、犯贫、窃听器、小虫等意思。现在人们将在电脑系统或程序中，隐藏着的一些未被发现的缺陷或问题统称为bug（漏洞）。 由于现在社会的发展，bug另有一种引申意义，用来形容某事物厉害的超乎想象，BUG可以使电脑系统崩溃、容易被施诈者攻击，现有修复漏洞的工具'),
('代码', '代码就是程序员用开发工具所支持的语言写出来的源文件，是一组由字符、符号或信号码元以离散形式表示信息的明确的规则体系。代码设计的原则包括唯一确定性、标准化和通用性、可扩充性与稳定性、便于识别与记忆、力求短小与格式统一以及容易修改等'),
('老白', '老白是一个正直可爱并且非常善良的美少女，为我们提供了非常大的帮助'),
('国际软件学院', '武汉大学国际软件学院是教育部、国家计委首批批准成立的国家示范性软件学院，是为了适应我国经济结构战略性调整的要求和软件产业发展对人才的迫切需要而建立的，旨在为我国软件产业发展带来新的推动力，支持国家“以信息化带动工业化”的战略部署，培养复合型、实用型、国际化的高层次软件人才');
insert into topic_recommend(recommend_time, topic_id) values(1469184324, 1);
insert into users(username, password, email, group_id) values('admin', '3730a91a9c5c657d81181a0ea4493d11', 'admin@admin.com', 0);


