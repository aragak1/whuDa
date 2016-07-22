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

function checkmail(email) {
    var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    if(!myreg.test(email))
    {
        return false;
    }
    else {
        return true;
    }
}

function checkusername(username) {
    var myreg = /^[a-zA-Z][a-zA-Z0-9]*$/;
    if(!myreg.test(username))
    {
        return false;
    }
    else {
        return true;
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

    if (username == '') {
        alert('用户名不能为空')
        return
    }
    if (password == '') {
        alert('密码不能为空')
        return
    }
    if (repeat_password == '') {
        alert('请再次确认密码')
        return
    }
    if (repeat_password != password) {
        alert('两次输入的密码不一致，请检查')
        return
    }
    if (email == '') {
        alert('邮箱不能为空')
        return
    }
    if (phone == '') {
        alert('电话不能为空')
        return
    }
    if (!checkusername(username)) {
        alert('用户名必须以字母开头')
        return
    }
    if (!checkmail(email)) {
        alert('邮箱格式不正确，请重新输入')
        return
    }
    document.forms["add_admin_form"].submit()
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

    if (username == '') {
        alert('用户名不能为空')
        return
    }
    if (password == '') {
        alert('密码不能为空')
        return
    }
    if (repeat_password == '') {
        alert('请再次确认密码')
        return
    }
    if (repeat_password != password) {
        alert('两次输入的密码不一致，请检查')
        return
    }
    if (email == '') {
        alert('邮箱不能为空')
        return
    }
    if (phone == '') {
        alert('电话不能为空')
        return
    }
    if (!checkusername(username)) {
        alert('用户名必须以字母开头')
        return
    }
    if (!checkmail(email)) {
        alert('邮箱格式不正确，请重新输入')
        return
    }
    document.forms["add_user_form"].submit()
}