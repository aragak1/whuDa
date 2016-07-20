/**
 * Created by terry on 16-7-19.
 */
function send_message() {
    var content = $('textarea[name="message"]').val()
    var recipient = $('input[name="recipient"]').val()
    var session_id = $('input[name="session_id"]').val()
    $.post('/message/send', {
        'content': content,
        'recipient': recipient,
        'session_id': session_id
    },function (status) {
        if (status == 'success') {
            alert('发送成功!')
        }
        else if (status == 'empty_content') {
            alert('私信内容不能为空!');
            location.reload()
        }
    })
}

function new_session() {
    $('#aw-ajax-box').children('.modal').slideDown(1000);
}

function close_new_session() {
    $('#aw-ajax-box').children('.modal').hide();
}

function send_new_session() {
    var recipient = $('#invite-input').val();
    var content = $('textarea[name="message"]').val();
    $.post('/message', {
        'recipient': recipient,
        'content': content
    }, function (status) {
        if (status == 'not_exist_user') {
            alert('不存在该用户！');
        }
        else if (status == 'empty_content') {
            alert('内容不能为空');
        }
        else if (status == 'success') {
            $('#aw-ajax-box').children('.modal').hide();
            alert('私信发送成功！');
            location.reload()
        }
    })
}