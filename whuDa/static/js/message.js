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
            swal({
                title:'发送成功',
                type:'success',
                confirmButtonText:'确定',
                confirmButtonColor:'#499ef3'
            }, function () {
                location.reload();
            });
        }
        else if (status == 'empty_content') {
            swal({
                title:'发送失败',
                text:'私信内容不能为空',
                type:'error',
                confirmButtonText:'确定',
                confirmButtonColor:'#499ef3'
            });
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
            swal({
                title:'发送失败',
                text:'不存在该用户',
                type:'error',
                confirmButtonText:'确定',
                confirmButtonColor:'#499ef3'
            });
        }
        else if (status == 'empty_content') {
            swal({
                title:'发送失败',
                text:'内容不能为空',
                type:'error',
                confirmButtonText:'确定',
                confirmButtonColor:'#499ef3'
            });
        }
        else if (status == 'success') {
            $('#aw-ajax-box').children('.modal').hide();
            swal({
                title:'发送成功',
                type:'success',
                confirmButtonText:'确定',
                confirmButtonColor:'#499ef3'
            }, function () {
                location.reload();
            });
        }
    })
}

function delete_session(obj) {
    swal({
        title: '确定要删除吗？',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定",
        closeOnConfirm: false,
        cancelButtonText: '取消'
    }, function () {
        var session_id = obj.getAttribute('data-id');
        $.post('/session/delete', {
            'session_id': session_id
        }, function (status) {
            if (status == 'success') {
                swal({
                    title: '删除成功',
                    type: 'success',
                    confirmButtonText: '确定',
                    confirmButtonColor: '#499ef3'
                }, function () {
                    location.reload();
                });
            }
            else if (status == 'error') {
                swal({
                    title: '删除失败',
                    type: 'error',
                    confirmButtonText: '确定',
                    confirmButtonColor: '#499ef3'
                });
            }
        });
    });
}