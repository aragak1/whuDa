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

    //
    // // 文本框失去焦点
    // $('#aw_edit_topic_title').blur(function () {
    //     $('#edit_topic_title_div').children('p.title').hide();
    //     $('#edit_topic_title_div').hide();
    //     $('#edit_topic_title_div').children('ul.aw-dropdown-list').hide();
    // });

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
                    alert('上传成功！');
                    location.reload();
                }
           },
           error:function(data){
               alert('上传失败！');
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
                alert('用户名不能为空')
            }
            else if (result == 'error2') {
                alert('邮箱不能为空')
            }
            else if (result == 'error3') {
                alert('密码不能为空')
            }
            else if (result == 'error4') {
                alert('请再次确认密码')
            }
            else if (result == 'error5') {
                alert('两次输入的密码不一致！')
                location.reload()
            }
            else if (result == 'error6') {
                alert('用户名必须以字母开头')
            }
            else if (result == 'error7') {
                alert('邮箱名非法，请正确填写')
            }
            else if (result == 'error8') {
                alert('用户名或者邮箱已存在，请重新输入！')
                location.reload()
            }
            else {
                alert('注册成功！')
                location.href = '/'
            }
        }
    )
};

function login() {
    var username = $('#l_username').val()
    var password = $('#l_password').val()
    $.post('/login',{
            username:username,
            password:password,
        },function (result) {
            if (result == 'error1')
            {
                alert('用户名不能为空')
            }
            else if (result == 'error2')
            {
                alert('密码不能为空')
            }
            else if (result == 'success'){
                location.href = '/'
            }
            else {
                alert('用户名或密码错误！')
                location.reload()
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
            alert('标题不能为空')
        }
        else if (status == 'empty_topics') {
            alert('至少应该选择一个话题')
        }
        else if(status == 'empty_content') {
            alert('请填写回复内容')
        }
        else{
            alert('发布成功')
            location.href = '/question/' + status
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
            alert('你已经回复过这个问题')
            location.reload()
        }
        else {
            alert('回复成功')
            location.reload()
        }
    })
}

function c_all_more() {
    var next_page = current_c_all_more_page + 1;
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

function user_question_more() {
    var next_page = current_question_more_page + 1;
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
                list_html += '<a href="/question/'+ obj[i].question_id +'" class="pull-right text-color-999">回复</a><p>'
                list_html += '<a href="/people'+ obj[i].user_url +'" class="aw-user-name">'+ obj[i].dynamic_str +'</a>'
                list_html += '<span class="text-color-999"> • '+ obj[i].question_focus_count +' 人关注 • '+ obj[i].question_answer_count +' 个回复 • '+ obj[i].question_view_count +' 次浏览 • '+ obj[i].publish_time +'</span>'
                list_html += '</p></div></div>'
                $('#user_focus_question_more_list').append(list_html);
            }
        }
    })
}

function user_focus_topic_more() {
    
}

function user_latest_activity_more() {
    
}

function switch_tab(flag) {
    if (flag == 1)
    {
        var a = document.getElementById("user_focus_question_more_list")
        a.style.display = 'block'
        var b = document.getElementById("user_focus_question_more")
        b.style.display = 'none'
    }
    else {
        var a = document.getElementById("user_focus_question_more_list")
        a.style.display = 'none'
        var b = document.getElementById("user_focus_question_more")
        b.style.display = 'block'
    }
}

