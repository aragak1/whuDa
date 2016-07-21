function deleteTopic(obj) {
    var r = confirm("确定要删除这个话题吗？请谨慎操作!");
    if (r == true) {
        var topic_id = obj.getAttribute('data-topicId')
        $.post('/admin/topic/delete', {
            'topic_id':topic_id
        }, function (result) {
            if (result == 'success') {
                alert('删除成功！');
                location.reload();
            } else if (result == 'error') {
                alert('删除失败!');
            } else if (result == 'not_null') {
                alert('话题下问题数不为0，无法删除!');
            }
        })
    } else {
        location.reload()
    }
}

function add_admin() {
    var username = $('#username').val()
    var password = $('#password').val()
    var repeat_password = $('#repeat_password').val()
    var sex = $('#sex').val()
    var birthday_y = $('#birthday_y').val()
    var birthday_m = $('#birthday_m').val()
    var birthday_d = $('#birthday_d').val()
    var department_id = $('#department_id').val()
    var brief = $('#brief').val()
    var email = $('#email').val()
    var qq = $('#qq').val()
    var phone = $('#phone').val()
    var website = $('#website').val()

    $.post('/admin/manage_admin/add',
        {
            username:username,
            password:password,
            repeat_password:repeat_password,
            sex:sex,
            birthday_y:birthday_y,
            birthday_m:birthday_m,
            birthday_d:birthday_d,
            department_id:department_id,
            brief:brief,
            email:email,
            qq:qq,
            phone:phone,
            website:website
        },function (result) {
            if (result == 'error1') {
                alert('用户名不能为空')
            }
            else if (result == 'error2') {
                alert('密码不能为空')
            }
            else if (result == 'error3') {
                alert('请再次确认密码')
            }
            else if (result == 'error4') {
                alert('两次输入的密码不一致！')
            }
            else if (result == 'error5') {
                alert('邮箱不能为空')
            }
            else if (result == 'error6') {
                alert('qq不能为空')
            }
            else if (result == 'error7') {
                alert('电话不能为空')
            }
            else if (result == 'error8') {
                alert('用户名必须以字母开头')
            }
            else if (result == 'error9') {
                alert('邮箱名非法，请检查')
            }
            else {
                alert('注册成功！')
                location.href = '/admin/manage_admin/page/1'
            }
        }
    )
}

function add_general_user() {
    var username = $('#username').val()
    var password = $('#password').val()
    var repeat_password = $('#repeat_password').val()
    var sex = $('#sex').val()
    var birthday_y = $('#birthday_y').val()
    var birthday_m = $('#birthday_m').val()
    var birthday_d = $('#birthday_d').val()
    var department_id = $('#department_id').val()
    var brief = $('#brief').val()
    var email = $('#email').val()
    var qq = $('#qq').val()
    var phone = $('#phone').val()
    var website = $('#website').val()

    $.post('/admin/manage_user/add',
        {
            username:username,
            password:password,
            repeat_password:repeat_password,
            sex:sex,
            birthday_y:birthday_y,
            birthday_m:birthday_m,
            birthday_d:birthday_d,
            department_id:department_id,
            brief:brief,
            email:email,
            qq:qq,
            phone:phone,
            website:website
        },function (result) {
            if (result == 'error1') {
                alert('用户名不能为空')
            }
            else if (result == 'error2') {
                alert('密码不能为空')
            }
            else if (result == 'error3') {
                alert('请再次确认密码')
            }
            else if (result == 'error4') {
                alert('两次输入的密码不一致！')
            }
            else if (result == 'error5') {
                alert('邮箱不能为空')
            }
            else if (result == 'error6') {
                alert('qq不能为空')
            }
            else if (result == 'error7') {
                alert('电话不能为空')
            }
            else if (result == 'error8') {
                alert('用户名必须以字母开头')
            }
            else if (result == 'error9') {
                alert('邮箱名非法，请检查')
            }
            else {
                alert('注册成功！')
                location.href = '/admin/manage_user/page/1'
            }
        }
    )
}