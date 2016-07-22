function deleteTopic(obj) {
    var sure = confirm("确定要删除这个话题吗？请谨慎操作!");
    if (sure == true) {
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
        swal({
            title: '添加失败',
            text: '用户名不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (password == '') {
        swal({
            title: '添加失败',
            text: '密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password == '') {
        swal({
            title: '添加失败',
            text: '请再次输入密码',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password != password) {
        swal({
            title: '添加失败',
            text: '两次输入的密码不一致，请检查',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (email == '') {
        swal({
            title: '添加失败',
            text: '邮箱不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (phone == '') {
        swal({
            title: '添加失败',
            text: '电话不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkusername(username)) {
        swal({
            title: '添加失败',
            text: '用户名必须以字母开头',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkmail(email)) {
        swal({
            title: '添加失败',
            text: '邮箱格式不正确，请重新输入',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
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
        swal({
            title: '添加失败',
            text: '用户名不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (password == '') {
        swal({
            title: '添加失败',
            text: '密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password == '') {
        swal({
            title: '添加失败',
            text: '请再次输入密码',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password != password) {
        swal({
            title: '添加失败',
            text: '两次输入的密码不一致，请检查',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (email == '') {
        swal({
            title: '添加失败',
            text: '邮箱不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (phone == '') {
        swal({
            title: '添加失败',
            text: '电话不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkusername(username)) {
        swal({
            title: '添加失败',
            text: '用户名必须以字母开头',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkmail(email)) {
        swal({
            title: '添加失败',
            text: '邮箱格式不正确，请重新输入',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    document.forms["add_user_form"].submit()
}

function update_admin() {
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
        swal({
            title: '修改失败',
            text: '用户名不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (password == '') {
        swal({
            title: '修改失败',
            text: '密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password == '') {
        swal({
            title: '修改失败',
            text: '请再次输入密码',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password != password) {
        swal({
            title: '修改失败',
            text: '两次输入的密码不一致，请检查',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (email == '') {
        swal({
            title: '修改失败',
            text: '邮箱不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (phone == '') {
        swal({
            title: '修改失败',
            text: '电话不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkusername(username)) {
        swal({
            title: '修改失败',
            text: '用户名必须以字母开头',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkmail(email)) {
        swal({
            title: '修改失败',
            text: '邮箱格式不正确，请重新输入',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    document.forms["update_admin_form"].submit()
}

function update_general_user() {
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
        swal({
            title: '修改失败',
            text: '用户名不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (password == '') {
        swal({
            title: '修改失败',
            text: '密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password == '') {
        swal({
            title: '修改失败',
            text: '请再次确认密码',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_password != password) {
        swal({
            title: '修改失败',
            text: '两次输入的密码不一致，请检查',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (email == '') {
        swal({
            title: '修改失败',
            text: '邮箱不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (phone == '') {
        swal({
            title: '修改失败',
            text: '电话不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkusername(username)) {
        swal({
            title: '修改失败',
            text: '用户名必须以字母开头',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (!checkmail(email)) {
        swal({
            title: '修改失败',
            text: '邮箱格式不正确',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    document.forms["update_user_form"].submit()
}

function deleteUser(obj) {
    swal({
        title: '确定要删除吗？',
        text: '该操作不可逆转，请谨慎使用',
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定",
        closeOnConfirm: false,
        cancelButtonText: '取消'
    }, function () {
        var uid = obj.getAttribute('data-uid')
        $.post('/admin/user/delete', {
            'uid':uid
        }, function (result) {
            if (result == 'success') {
                swal({
                    title: '删除成功',
                    type: 'success',
                    confirmButtonText: '确定',
                    confirmButtonColor: '#337ab7'
                }, function () {
                    location.reload();
                });
            }
            else {
                swal({
                    title: '删除失败',
                    type: 'error',
                    confirmButtonText: '确定',
                    confirmButtonColor: '#337ab7'
                });
            }
        })
    })
}

function update_password() {
    var old_pwd = $('#old_pwd').val()
    var new_pwd = $('#new_pwd').val()
    var repeat_new_pwd = $('#repeat_new_pwd').val()
    if (old_pwd == '') {
        swal({
            title: '修改失败',
            text: '原密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (new_pwd == '') {
        swal({
            title: '修改失败',
            text: '新密码不能为空',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (repeat_new_pwd == '') {
        swal({
            title: '修改失败',
            text: '请再次输入新密码',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    if (new_pwd != repeat_new_pwd) {
        swal({
            title: '修改失败',
            text: '两次输入的新密码不一致，请检查',
            type: 'error',
            confirmButtonText: '确定',
            confirmButtonColor: '#337ab7'
        });
        return false;
    }
    $.post('/admin/update_password', {
        'uid':uid,
        'old_pwd':old_pwd,
        'new_pwd':new_pwd,
        'repeat_new_pwd':repeat_new_pwd
    }, function (result) {
        if (result == 'success') {
            swal({
                title: '修改成功',
                type: 'success',
                confirmButtonText: '确定',
                confirmButtonColor: '#337ab7'
            }, function () {
                if (flag == 1) {
                    location.href = '/admin/manage_admin/page/1'
                } else {
                    location.href = '/admin/manage_user/page/1'
                }
            });

        }
        else {
            swal({
                title: '修改失败',
                text: '原密码不正确',
                type: 'error',
                confirmButtonText: '确定',
                confirmButtonColor: '#337ab7'
            });
            return false;
        }
    })
}