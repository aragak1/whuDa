/*
 * 页面监听*/
$(document).ready(function () {
    // 文本框内容发生改变
    $('#aw_edit_topic_title').bind('input propertychange', function () {
        if ($('#aw_edit_topic_title').val() != '') {
            var keyword = $('#aw_edit_topic_title').val();
            $.post('/api/topic/find/' + keyword + '.find', function (result) {
                if (result == 'success') {
                    $('#edit_topic_title_div').children('p.title').hide();
                    $('#edit_topic_title_div').children('ul.aw-dropdown-list').empty();
                    $.getJSON('/api/topic/like/' + keyword + '.json', function (data) {
                        $.each(data.topics, function (i, item) {
                            $('#edit_topic_title_div').children('ul.aw-dropdown-list').append('<li class="question"><a><b class="active">' + item.name + '</b></a></li>')
                        })
                    })
                    $('#edit_topic_title_div').children('ul').show();
                    $('#edit_topic_title_div').show();
                }
                else{
                    $('#edit_topic_title_div').children('ul.aw-dropdown-list').hide();
                    $('#edit_topic_title_div').children('p.title').show();
                }
            })}
        else {
            $('#edit_topic_title_div').hide();
        }
    });

    // 添加topic tags
    $(document).on('click', '.question', function () {
        var topic_name = $(this).text();
        $('#pb_tag-bar').append('<span class="topic-tag"><a class="text">' +
            topic_name + '</a><a class="close" onclick="$(this).parents(\'.topic-tag\').remove();">' +
            '<i class="icon icon-delete"></i></a><input type="hidden" value="' +
            topic_name + '" name="topics[]"></span>');
    });

    //绑定了`submit`事件。
    $('#upload-form').on('submit',(function(e) {
        e.preventDefault();
        //序列化表单
        var serializeData = $(this).serialize();

        // var formData = new FormData(this);
        $(this).ajaxSubmit({
            type:'POST',
            url: '/user/avatar/upload',
            data: serializeData,
            contentType: false,
            cache: false,
            processData:false,

            success:function(data){
                if (data='success'){
                    swal({
                        title:'上传成功',
                        type:'success',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    }, function () {
                        location.reload()
                    })
                }
            },
            error:function(data){
                swal({
                        title:'上传失败',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
        });
    }));

    //绑定文件选择事件，一选择了图片，就让`form`提交。
    $("#upload_file").on("change", function() {
        $(this).parent().submit();
    });

});


/*
 * 自定义函数*/
function register() {
    var username = $('#username').val()
    var password = $('#password').val()
    var repeat_password = $('#repeat_password').val()
    var email = $('#email').val()

    $.post('/register',
        {
            username:username,
            password:password,
            repeat_password:repeat_password,
            email:email
        },function (result) {
            if (result == 'error1') {
                swal({
                        title:'注册失败',
                        text:'用户名不能为空',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error2') {
                swal({
                        title:'注册失败',
                        text:'邮箱不能为空',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error3') {
                swal({
                        title:'注册失败',
                        text:'密码不能为空',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error4') {
                swal({
                        title:'注册失败',
                        text:'请再次确认密码',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error5') {
                swal({
                        title:'注册失败',
                        text:'两次输入的密码不一致！',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    }, function () {
                    location.href = '/register'
                })
            }
            else if (result == 'error6') {
                swal({
                        title:'注册失败',
                        text:'用户名必须以字母开头',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error7') {
                swal({
                        title:'注册失败',
                        text:'邮箱名非法，请正确填写',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    })
            }
            else if (result == 'error8') {
                swal({
                        title:'注册失败',
                        text:'用户名或者邮箱已存在，请重新输入！',
                        type:'error',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    }, function () {
                    location.href = '/register'
                })
            }
            else {
                swal({
                        title:'注册成功',
                        type:'success',
                        confirmButtonText:'确定',
                        confirmButtonColor:'#499ef3'
                    }, function () {
                    location.href = '/'
                })
            }
        }
    )
}

function login() {
    var username = $('#l_username').val()
    var password = $('#l_password').val()
    $.post('/login',{
            username:username,
            password:password,
        },function (result) {
            if (result == 'error1')
            {
                swal({
                    title:'登陆失败',
                    text:'用户名不能为空',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
            }
            else if (result == 'error2')
            {
                swal({
                    title:'登陆失败',
                    text:'密码不能为空',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
            }
            else if (result == 'success'){
                location.href = '/'
            }
            else {
                swal({
                    title:'登陆失败',
                    text:'用户名或密码错误！',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                    location.href = '/login'
                })
            }
        }
    )
};

function publish_question() {
    var title = $('#question_contents').val()
    var content =  editor.$txt.html();
    var topics = new Array()
    var is_anonymous = 0
    $('a.text').each(function () {
        topics.push($(this).text())
    });
    if ($('#is_anonymous').is(':checked')){
        is_anonymous = 1
    }
    $.post('/publish/question',{
        title:title,
        content:content,
        'topics[]':topics,
        anonymous:is_anonymous
    },function (status) {
        if (status == 'empty_title') {
            swal({
                    title:'发布失败',
                    text:'标题不能为空',
                    type:'warning',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'empty_topics') {
            swal({
                    title:'发布失败',
                    text:'至少应该选择一个话题',
                    type:'warning',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if(status == 'empty_content') {
            swal({
                    title:'发布失败',
                    text:'请填写回复内容',
                    type:'warning',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else{
            swal({
                    title:'发布成功',
                    type:'success',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                location.href = '/question/' + status
            });
        }
    });
};

function publish_comment() {
    var question_id = $('#question_id').val()
    var answer_content =  editor.$txt.html()
    var is_anonymous = 0
    var focus_question = 1
    if ($('#is_anonymous').is(':checked')) {
        is_anonymous = 1
    }
    if ($('#auto_focus').is(':checked')) {
        focus_question = 0
    }
    $.post('/question/answer',{
        question_id:question_id,
        answer_content:answer_content,
        is_anonymous:is_anonymous,
        focus_question:focus_question
    },function (status) {
        if (status == 'answered') {
            swal({
                    title:'评论失败',
                    text:'你已经回复过这个答案',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                location.reload()
            });
        }
        else {
            swal({
                    title:'回复成功',
                    type:'success',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                location.reload()
            });
        }
    })
}

function c_all_more() {
    var next_page = current_c_all_more_page + 1;
    current_c_all_more_page++;
    var topic_id = topic_detail_page_topic_id
    var post_url = '/api/topic/' + topic_id + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#c_all_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item">'
                if (obj[i].is_anonymous == 1) {
                    list_html += '<a class="aw-user-name hidden-xs" href="/people"><img src="/static/img/avatar/avatar.png" alt="匿名用户" title="匿名用户" /></a>'
                }
                else {
                    list_html += '<a class="aw-user-name hidden-xs" href="/people'+ obj[i].user_url +'"><img src="'+ obj[i].avatar_url + '" /></a>'
                }
                list_html += '<div class="aw-question-content"><h4><a href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a></h4>'
                list_html += '<a href="/question/'+ obj[i].question_id +'" class="pull-right text-color-999">回复</a><p>'
                list_html += '<a href="/people'+ obj[i].user_url +'" class="aw-user-name">'+ obj[i].dynamic_str +'</a>'
                list_html += '<span class="text-color-999"> • '+ obj[i].question_focus_count +' 人关注 • '+ obj[i].question_answer_count +' 个回复 • '+ obj[i].question_view_count +' 次浏览 • '+ obj[i].publish_time +'</span>'
                list_html += '</p></div></div>'
                $('#c_all_list').append(list_html);
            }
        }
    })
}

function c_more_dynamic(){
    var next_page = current_dynamic_page + 1
    current_dynamic_page++
    var uid = user_uid
    var post_url = '/api/dynamic/'+ uid + '/page/' + next_page + '.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#bp_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item"><div class="mod-head">'
                if (obj[i].is_anonymous == 1) {
                    list_html += '<a class="aw-user-img aw-border-radius-5" href="/people'+ obj[i].user_url +'"><img src="/static/img/avatar/avatar.png"></a>'
                    list_html += '<p class="text-color-999">'
                    list_html += '<a href="/people'+ obj[i].user_url + '" class="aw-user-name">'+ obj[i].dynamic_str +'</a> • '+ obj[i].publish_time +' •'
                }
                else {
                    list_html += '<a class="aw-user-img aw-border-radius-5" href="/people' + obj[i].user_url  + '"><img src="/' + obj[i].avatar_url + '"></a>'
                    list_html += '<p class="text-color-999">'
                    list_html += '<a href="/people'+ obj[i].user_url +'" class="aw-user-name">'+ obj[i].dynamic_str +'</a> • '+ obj[i].publish_time +' •'
                }
                list_html += '<a href="/question/'+ obj[i].question_id +'" class="text-color-999">'+ obj[i].question_answer_count +' 个回复</a></p>'
                list_html += '<h4><a href="/question/'+ obj[i].question_uid +'">'+ obj[i].title +'</a></h4>'
                list_html += '<div class="meta clearfix">'
                list_html += '<span class="pull-right more-operate">'
                list_html += '<a href="javascript:;" onclick="add_question_to_favorite(user_uid, '+ obj[i].question_id +')" class="text-color-999"><i class="icon icon-favor"></i>收藏该问题</a>'
                list_html += '<a class="text-color-999 dropdown-toggle" data-toggle="dropdown"></a>'
                list_html += '</span></div></div></div>'
                $('#main_contents').append(list_html)
            }
        }
    })
}

function user_question_more() {
    var next_page = current_question_more_page + 1;
    current_question_more_page++
    var uid = people_id
    var post_url = '/api/user_question/' + uid + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#user_question_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item"><div class="mod-head">'
                list_html += '<h4><a href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a></h4></div>'
                list_html += '<div class="mod-body">'
                list_html += '<span class="aw-border-radius-5 count pull-left"><i class="icon icon-reply"></i>&nbsp;'+ obj[i].reply_count +'</span>'
                list_html += '<p class="aw-hide-txt">'+ obj[i].view_count +' 次浏览 &nbsp;• '+ obj[i].focus_count +' 个关注 &nbsp; • '+ obj[i].publish_time +'前</p>'
                list_html += '</div></div>'
                $('#user_question_more_list').append(list_html);
            }
        }
    })
}

function user_answer_more() {
    var next_page = current_answer_more_page + 1;
    current_answer_more_page++
    var uid = people_id
    var post_url = '/api/user_answer/' + uid + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#user_answer_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item"><div class="mod-head">'
                list_html += '<h4><a href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a></h4>'
                list_html += '</div><div class="mod-body">'
                list_html += '<span class="aw-border-radius-5 count pull-left"><i class="icon icon-agree"></i>&nbsp;'+ obj[i].agree_count +'</span>'
                list_html += '<p style="max-width: 610px">'+ obj[i].content +'</p>'
                list_html += '</div></div>'
                $('#user_answer_more_list').append(list_html);
            }
        }
    })
}

function user_focus_question_more() {
    var next_page = current_focus_question_more_page + 1;
    current_focus_question_more_page++
    var uid = people_id
    var post_url = '/api/user_focus_question/' + uid + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#user_focus_question_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item">'
                if (obj[i].is_anonymous == 1) {
                    list_html += '<a class="aw-user-name hidden-xs" href="/people"><img src="/static/img/avatar/avatar.png" alt="匿名用户" title="匿名用户" /></a>'
                }
                else {
                    list_html += '<a class="aw-user-name hidden-xs" href="/people'+ obj[i].user_url +'"><img src="'+ obj[i].avatar_url + '" /></a>'
                }
                list_html += '<div class="aw-question-content"><h4><a href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a></h4>'
                list_html += '<a href="/people'+ obj[i].user_url +'" class="aw-user-name">'+ obj[i].dynamic_str +'</a>'
                list_html += '<span class="text-color-999"> • '+ obj[i].question_focus_count +' 人关注 • '+ obj[i].question_answer_count +' 个回复 • '+ obj[i].question_view_count +' 次浏览 • '+ obj[i].publish_time +'</span>'
                list_html += '</p></div></div>'
                $('#user_focus_question_more_list').append(list_html);
            }
        }
    })
}

function user_latest_activity_more() {
    var next_page = current_latest_activity_more_page + 1;
    current_latest_activity_more_page++
    var uid = people_id
    var post_url = '/api/user_latest_activity/' + uid + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#user_latest_activity_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<li><p>'
                if (obj[i].is_question) {
                    list_html += '<span class="pull-right text-color-999">'+ obj[i].last_time +'前</span>'
                    list_html += '<em class="pull-left"><a href="/people/'+ obj[i].username +'" class="aw-user-name">'+ obj[i].username +' </a> 提出了问题,&nbsp;</em>'
                    list_html += '<a class="aw-hide-txt" href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a>'
                }
                else {
                    list_html += '<span class="pull-right text-color-999">'+ obj[i].last_time +'前</span>'
                    list_html += '<em class="pull-left"><a href="/people/'+ obj[i].username +'" class="aw-user-name">'+ obj[i].username +' </a> 回答了问题,&nbsp;</em>'
                    list_html += '<a class="aw-hide-txt" href="/question/'+ obj[i].question_id +'">'+ obj[i].title +'</a>'
                }
                list_html += '</p></li>'
                $('#user_latest_activity_more_list').append(list_html);
            }
        }
    })
}

function update_user_profile() {
    var sex = $('input[name="sex"]:checked').val()
    var birth_year = $('select[name="birthday_y"]').find("option:selected").val()
    var birth_month = $('select[name="birthday_m"]').find("option:selected").val()
    var birth_day = $('select[name="birthday_d"]').find("option:selected").val()
    var introduction = $('input[name="signature"]').val()
    var qq = $('#input-qq').val()
    var moblie = $('#input-mobile').val()
    var website = $('#input-homepage').val()
    var department_id = $('#department').find('option:selected').val()

    $.post('/user/profile/update', {
        'sex':sex,
        'birth_year': birth_year,
        'birth_day': birth_day,
        'birth_month': birth_month,
        'introduction': introduction,
        'qq': qq,
        'mobile': moblie,
        'website': website,
        'department_id': department_id
    }, function (status) {
        if (status == 'error_qq') {
            swal({
                    title:'更改失败',
                    text:'错误的qq号！',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'error_mobile') {
            swal({
                    title:'更改失败',
                    text:'错误的手机号！',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'success') {
            swal({
                    title:'更改成功',
                    type:'success',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                location.reload()
            });
        }
    })
}

function change_pass() {
    var old_password = $('#input-password-old').val()
    var new_password = $('#input-password-new').val()
    var re_new_password = $('#input-password-re-new').val()
    $.post('/user/change/password', {
        'old_password': old_password,
        'new_password': new_password,
        're_password': re_new_password
    }, function (status) {
        if (status == 'not_same') {
            swal({
                    title:'更改失败',
                    text:'两次输入的密码不一致',
                    type:'warning',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'old_empty') {
            swal({
                    title:'更改失败',
                    text:'原密码不能为空',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'new_empty') {
            swal({
                    title:'更改失败',
                    text:'新密码不能为空',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 're_empty') {
            swal({
                    title:'更改失败',
                    text:'请再次重复新密码',
                    type:'warning',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'error_pass') {
            swal({
                    title:'更改失败',
                    text:'原密码输入不正确',
                    type:'error',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
        else if (status == 'success') {
            swal({
                    title:'密码更改成功',
                    type:'success',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                }, function () {
                location.reload()
            });
        }
    })
}

function user_focus_topics_more() {
    var next_page = current_user_focus_topic_more_page + 1;
    current_user_focus_topic_more_page++
    var uid = user_uid
    var post_url = '/api/user_focus_topic/' + uid + '/page/'+ next_page +'.json'
    $.getJSON(post_url, function (datas) {
        if (jQuery.isEmptyObject(datas)){
            $('#user_focus_topics_more').children('span').text('没有更多了');
        }
        else {
            var obj = eval(datas)
            for (var i=0; i<obj.length; i++) {
                var list_html = '<div class="aw-item">'
                list_html += '<a class="img aw-border-radius-5" href="/topic/'+ obj[i].topic_id +'">'
                list_html += '<img src="/'+ obj[i].topic_url +'" alt="'+ obj[i].topic_name +'" />'
                list_html += '</a><p class="clearfix"><span class="topic-tag">'
                list_html += '<a class="text" href="/topic/'+ obj[i].topic_id +'">'+ obj[i].topic_name +'</a>'
                list_html += '</span></p><p class="text-color-999">'
                list_html += '<span>'+ obj[i].topic_question_count +' 个问题</span>'
                list_html += '<span>'+ obj[i].topic_focus +' 个关注</span>'
                list_html += '</p>'
                list_html += '<p class="text-color-999">7 天新增 '+ obj[i].last_week_question_count +' 个问题, 30 天新增 '+ obj[i].last_month_question_count +' 个问题 </p>'
                list_html += '</div>'
                $('#user_focus_topic_list').append(list_html);
            }
        }
    })
}

function global_search() {
    var keyword = $('#aw-search-query').val()
    if (keyword == '' || keyword.replace(/^\s+|\s+$/g,"").length == 0) {
        return
    }
    location.href = '/search/' + keyword
}

function add_question_to_favorite(uid, question_id) {
    $.post('/add_to_favor',{
        uid:uid,
        question_id:question_id
    },function (status) {
        if (status == 'success') {
            swal({
                    title:'收藏成功',
                    type:'success',
                    confirmButtonText:'确定',
                    confirmButtonColor:'#499ef3'
                });
        }
    })
}